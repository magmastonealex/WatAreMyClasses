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


public class MapActivity extends ActionBarActivity implements OnMapReadyCallback,GoogleApiClient.ConnectionCallbacks, GoogleApiClient.OnConnectionFailedListener, LocationListener,SensorEventListener {
    private SensorManager mSensorManager;
    private GoogleApiClient mGoogleApiClient;
    private float[] mRotationMatrix = new float[16];
    private float mDeclination;
    private GoogleMap map;
    private NetworkInteractor ni;
    private OfflineCacher oC;
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

       // mSensorManager.registerListener(this, rotSense, 400000);

        ni = new NetworkInteractor();
        TokenStorage tS = new TokenStorage(this);
        oC=new OfflineCacher(tS.getUserID(),tS.getToken(),ni);
        oC.doCache();


    }
    @Override
    public final void onAccuracyChanged(Sensor sensor, int accuracy) {
        // Do something here if sensor accuracy changes.
    }

    @Override
    public final void onSensorChanged(SensorEvent event) {
        // The light sensor returns a single value.
        // Many sensors return 3 values, one for each axis.
        // Do something with this sensor value.
        if(event.sensor.getType() == Sensor.TYPE_ROTATION_VECTOR) {
            SensorManager.getRotationMatrixFromVector(
                    mRotationMatrix , event.values);
            float[] orientation = new float[3];
            SensorManager.getOrientation(mRotationMatrix, orientation);
            float bearing = (float)Math.toDegrees(orientation[0]) + mDeclination;

            updateCamera(bearing);
        }
    }
    private void updateCamera(float bearing) {
        CameraPosition oldPos = map.getCameraPosition();

        CameraPosition pos = CameraPosition.builder(oldPos).bearing(bearing).build();

        map.moveCamera(CameraUpdateFactory.newCameraPosition(pos));
    }
    @Override
    public void onConnectionFailed(ConnectionResult result) {
        Log.i("MapActivity", "Connection failed: ConnectionResult.getErrorCode() = "
                + result.getErrorCode());
    }

    @Override
    public void onConnected(Bundle arg0) {
        startLocationUpdates();

        Location lastLoc = LocationServices.FusedLocationApi.getLastLocation(mGoogleApiClient);
        ni.webservice.getClosestNode(String.valueOf(lastLoc.getLatitude()),String.valueOf(lastLoc.getLongitude()), new Callback<WatNode>() {
            @Override
            public void success(WatNode watNode, Response response) {
                Log.d("MapActivity","Found closest node: "+watNode.id);
                pathWithClosestNode(watNode);
            }

            @Override
            public void failure(RetrofitError error) {
                   Log.e("MapActivity","Failed to find closest node");
            }
        });
        // Once connected with google api, get the location

    }
    protected  void pathWithClosestNode(WatNode node){
        ni.webservice.getPath(node.id,"b-SLC",new Callback<List<WatNode>>() {
            @Override

            public void success(List<WatNode> watNodes, Response response) {
                Log.d("MapActivity","Found path!");
                ArrayList<LatLng> points=new ArrayList<LatLng>();
                for(WatNode nde : watNodes){
                    Log.d("MapActivity","Node:"+nde.id);
                    points.add(new LatLng(Double.valueOf(nde.lat),Double.valueOf(nde.lon)));
                }

                Polyline lne=map.addPolyline(new PolylineOptions()
                .width(10)
                .color(Color.RED)
                );
                lne.setPoints(points);
            }

            @Override
            public void failure(RetrofitError error) {
                Log.e("MapActivity","Error getting path!: "+error.getLocalizedMessage());
            }
        });
    }
    protected void startLocationUpdates() {
        LocationRequest mLocationRequest = new LocationRequest();
        mLocationRequest.setInterval(10000);
        mLocationRequest.setFastestInterval(2000);
        mLocationRequest.setPriority(LocationRequest.PRIORITY_HIGH_ACCURACY);
        LocationServices.FusedLocationApi.requestLocationUpdates(mGoogleApiClient,mLocationRequest,this);
    }
    private void stopLocationUpdates(){
        LocationServices.FusedLocationApi.removeLocationUpdates(mGoogleApiClient,this);
    }
    @Override
    public void onLocationChanged(Location location) {
        GeomagneticField field = new GeomagneticField(
                (float)location.getLatitude(),
                (float)location.getLongitude(),
                (float)location.getAltitude(),
                System.currentTimeMillis()
        );
        // getDeclination returns degrees
        mDeclination = field.getDeclination();

            Log.d("MapActivity", "Location update:"+String.valueOf(location.getLatitude())+", "+String.valueOf(location.getLongitude()));

    }


    @Override
    public void onConnectionSuspended(int arg0) {
        mGoogleApiClient.connect();
    }

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


    }
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

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_buildings) {
            Intent intent = new Intent(this,BuildingList.class);
            ArrayList<WatBuilding> builds=new ArrayList<WatBuilding>(oC.buildings);

            intent.putExtra("buildings",builds);
            startActivity(intent);
            return true;
        }

        return super.onOptionsItemSelected(item);
    }
}
