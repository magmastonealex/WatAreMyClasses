package net.magmastone.wataremyclasses;

import android.content.Context;
import android.content.Intent;
import android.graphics.Color;
import android.hardware.GeomagneticField;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.location.Location;
import android.net.Network;
import android.os.Parcel;
import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.Toast;

import com.google.android.gms.common.ConnectionResult;
import com.google.android.gms.common.api.GoogleApiClient;
import com.google.android.gms.location.LocationListener;
import com.google.android.gms.location.LocationRequest;
import com.google.android.gms.location.LocationServices;
import com.google.android.gms.maps.CameraUpdate;
import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.MapFragment;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.model.CameraPosition;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.MarkerOptions;
import com.google.android.gms.maps.model.Polyline;
import com.google.android.gms.maps.model.PolylineOptions;

import net.magmastone.NetworkInteraction.Models.WatBuilding;
import net.magmastone.NetworkInteraction.Models.WatClass;
import net.magmastone.NetworkInteraction.Models.WatNode;
import net.magmastone.NetworkInteraction.NetworkInteractor;
import net.magmastone.Storage.OfflineCacher;
import net.magmastone.Storage.TokenStorage;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.text.DateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Map;

import retrofit.Callback;
import retrofit.RetrofitError;
import retrofit.client.Response;

/*
This ideally could use some refactoring work.

Grew from just Map into literally all the application logic + data input + navigation.

Major things:
    - Location stuff should probably be abstracted into another class, with a simple callback for new bearing availablity.
    - Generating Polylines (or even just generating LatLngs) from two nodes should be in another class.
    - Closest node should be abstracted away.

Minor things:
    - Need to check if user skipped before showing Schedule view activity. May be able to get away with a simple Toast.

 */
public class MapActivity extends ActionBarActivity implements OnMapReadyCallback,GoogleApiClient.ConnectionCallbacks, GoogleApiClient.OnConnectionFailedListener, LocationListener,SensorEventListener {
    private SensorManager mSensorManager;
    private GoogleApiClient mGoogleApiClient;
    private float[] mRotationMatrix = new float[16];
    private float mDeclination;
    private GoogleMap map;
    private NetworkInteractor ni;
    private OfflineCacher oC;
    private Polyline lne;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_map);

        MapFragment mapFragment = (MapFragment) getFragmentManager().findFragmentById(R.id.the_map);
        mapFragment.getMapAsync(this);
        mGoogleApiClient = new GoogleApiClient.Builder(this)
                .addConnectionCallbacks(this)
                .addOnConnectionFailedListener(this)
                .addApi(LocationServices.API).build();
        mGoogleApiClient.connect();

        mSensorManager = (SensorManager) getSystemService(Context.SENSOR_SERVICE);
        Sensor rotSense=mSensorManager.getDefaultSensor(Sensor.TYPE_ROTATION_VECTOR);

        mSensorManager.registerListener(this, rotSense, 400000);

        ni = new NetworkInteractor();
        TokenStorage tS = new TokenStorage(this);
        oC=new OfflineCacher(tS.getUserID(),tS.getToken(),ni,this);
        oC.doCache();

    
    }

    /*

    Sensor Things

    */
    @Override
    public final void onAccuracyChanged(Sensor sensor, int accuracy) {
        // Do something here if sensor accuracy changes.
    }

    //Smoothing value
    int cmpCount=0;

    @Override
    public final void onSensorChanged(SensorEvent event) {
        //Do some rather overly-complicated math to get True north bearing from a Rotation Vector sensor (which is relative to Magnetic north)
        if(event.sensor.getType() == Sensor.TYPE_ROTATION_VECTOR) {
            SensorManager.getRotationMatrixFromVector(
                    mRotationMatrix , event.values);
            float[] orientation = new float[3];
            SensorManager.getOrientation(mRotationMatrix, orientation);
            float bearing = (float)Math.toDegrees(orientation[0]) + mDeclination;
            if (cmpCount > 40) {
                cmpCount=0;
                updateCamera(bearing);
            }else {
                cmpCount++;
            }
        }
    }


    protected void startLocationUpdates() { //Called on onResume, as well as when it all starts.
        LocationRequest mLocationRequest = new LocationRequest();
        mLocationRequest.setInterval(10000); // Not particularly frequent. MapView has it's own update rate. This is only really required to figure out the declination for True North calculations.
        mLocationRequest.setFastestInterval(2000);
        mLocationRequest.setPriority(LocationRequest.PRIORITY_HIGH_ACCURACY); // Still need high accuracy. plus, higher accuracy means higher accuracy for closest node calculations.
        LocationServices.FusedLocationApi.requestLocationUpdates(mGoogleApiClient,mLocationRequest,this); //Begin.
    }
    private void stopLocationUpdates(){ // Called on onPause
        LocationServices.FusedLocationApi.removeLocationUpdates(mGoogleApiClient,this); //Stop while activity is in background.
    }
    //What to do when we get new lat/lon.
    int curTime=0;
    @Override
    public void onLocationChanged(Location location) {
        GeomagneticField field = new GeomagneticField( //Let Google do the math :)
                (float)location.getLatitude(),
                (float)location.getLongitude(),
                (float)location.getAltitude(),
                System.currentTimeMillis()
        );

        if(curTime==0){
            map.moveCamera(CameraUpdateFactory.newLatLng(new LatLng(location.getLatitude(),location.getLongitude())));
        }else{
            curTime=1;
        }
        if(location.hasBearing()){
            //updateCamera(location.getBearing());
           // Log.d("MapActivity","hadBearing");
        }
        map.animateCamera(CameraUpdateFactory.newLatLng(new LatLng(location.getLatitude(),location.getLongitude())));
        // getDeclination returns degrees
        mDeclination = field.getDeclination(); // Saved for reference when compass is used to rotate map.

    }

    @Override
    public void onConnectionSuspended(int arg0) {
        mGoogleApiClient.connect();
    } // Shouldn't ever happen. Still does.


    //Update camera on bearing change
    private void updateCamera(float bearing) {
        CameraPosition oldPos = map.getCameraPosition();

        CameraPosition pos = CameraPosition.builder(oldPos).bearing(bearing).build();

        map.animateCamera(CameraUpdateFactory.newCameraPosition(pos));
    }

    /*

    Google API things

    */
    @Override
    public void onConnectionFailed(ConnectionResult result) {
        Log.i("MapActivity", "Connection failed: ConnectionResult.getErrorCode() = "
                + result.getErrorCode());
    }

    @Override
    public void onConnected(Bundle arg0) { //App is licenced, our API key is valid, we're clear for launch.
        startLocationUpdates();
        this.setPathFromClosestToNode("b-SLC"); // Just for debug for now.
    }







    /*


    Map Things


     */
    @Override
    public void onMapReady(GoogleMap lmap) {
        map=lmap;
        // Add a marker in Sydney, Australia, and move the camera.
        map.getUiSettings().setCompassEnabled(true);
        map.setMapType(GoogleMap.MAP_TYPE_NORMAL);
        map.setMyLocationEnabled(true);
        LatLng sydney = new LatLng(43.471203, -80.543238);
        map.moveCamera(CameraUpdateFactory.newCameraPosition(
                CameraPosition.builder().target(sydney)
                        .zoom(18)
                        .tilt(80)
                        .build()));
        map.getUiSettings().setZoomControlsEnabled(true);
        map.getUiSettings().setZoomGesturesEnabled(false);
        map.getUiSettings().setMyLocationButtonEnabled(false);


    }

    //Set path from current location to given node, wiping out old PolyLine.
    private void setPathFromClosestToNode(final String to){
        Location lastLoc = LocationServices.FusedLocationApi.getLastLocation(mGoogleApiClient);
        if(lastLoc==null){
            Toast toast = Toast.makeText(getApplicationContext(), "You need location services enabled to use this app.", Toast.LENGTH_LONG); //Not avaialable.
            toast.show();
            return;
        }
        ni.webservice.getClosestNode(String.valueOf(lastLoc.getLatitude()),String.valueOf(lastLoc.getLongitude()), new Callback<WatNode>() {
            @Override
            public void success(WatNode watNode, Response response) {
                Log.d("MapActivity","Found closest node: "+watNode.id);
                ni.webservice.getPath(watNode.id, to, pathCback);
            }

            @Override
            public void failure(RetrofitError error) {
                Log.e("MapActivity","Failed to find closest node");
            }
        });
    }

    //Every time we get a list of WatNodes, it's always for a path. So this is a reusable version.
    private Callback<List<WatNode>> pathCback = new Callback<List<WatNode>>() {
        @Override

        public void success(List<WatNode> watNodes, Response response) {
            Log.d("MapActivity","Found path!");
            ArrayList<LatLng> points=new ArrayList<LatLng>();
            for(WatNode nde : watNodes){
                Log.d("MapActivity","Node:"+nde.id);
                points.add(new LatLng(Double.valueOf(nde.lat),Double.valueOf(nde.lon)));
            }
            if(lne != null) {
                lne.remove();
            }
            lne=map.addPolyline(new PolylineOptions()
                            .width(10)
                            .color(Color.RED)
            );
            lne.setPoints(points);


        }

        @Override
        public void failure(RetrofitError error) {
            Log.e("MapActivity","Error getting path!: "+error.getLocalizedMessage());
        }
    };


    /*

    General Activity housekeeping.


     */
    @Override
    public void onPause(){
        super.onPause();
        if(mGoogleApiClient.isConnected()) {
            stopLocationUpdates();
        }
    }
    @Override
    public void onResume(){
        super.onResume();
        oC.doCache();
        if(mGoogleApiClient.isConnected()){
            startLocationUpdates();
        }
    }
    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_map, menu);
        return true;
    }

    //Dispatch to other Activities
    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_buildings) {
            Intent intent = new Intent(this,BuildingList.class);
            if(oC.buildings != null) {
            ArrayList<WatBuilding> builds=new ArrayList<>(oC.buildings);
                intent.putExtra("buildings", builds);
                startActivityForResult(intent, 3);
            }else{
                Toast toast = Toast.makeText(getApplicationContext(), "Building list only available with internet connection! Relaunch the app with a connection.", Toast.LENGTH_LONG); //Not avaialable.
                toast.show();
            }
            return true;
        }else if (id == R.id.action_classes){
            Intent intent = new Intent(this,ScheduleViewActivity.class);
            if(oC.todayClasses != null) {
                ArrayList<WatClass> builds = new ArrayList<>(oC.todayClasses);
                intent.putExtra("classes", builds);
                startActivityForResult(intent, 3);
            }else{
                Toast toast = Toast.makeText(getApplicationContext(), "Schedule only available when signed in!", Toast.LENGTH_LONG); //Not avaialable.
                toast.show();
            }
        }

        return super.onOptionsItemSelected(item);
    }
    //What to do when we get a result
    //Oddly reusable...
    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        if(resultCode==RESULT_OK && requestCode==3){
            String nodeID= data.getStringExtra("nodeID");
            this.setPathFromClosestToNode(nodeID);
        }
    }
}
