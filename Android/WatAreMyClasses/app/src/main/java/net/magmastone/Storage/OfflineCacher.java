package net.magmastone.Storage;

import android.content.Context;
import android.widget.Toast;

import net.magmastone.NetworkInteraction.Models.WatBuilding;
import net.magmastone.NetworkInteraction.Models.WatClass;
import net.magmastone.NetworkInteraction.NetworkInteractor;

import java.util.HashMap;
import java.util.List;

import retrofit.Callback;
import retrofit.RetrofitError;
import retrofit.client.Response;

/**
 * Created by alex on 8/10/15.
 *
 * This caches the BuildingList and the day's schedule.
 *
 * Intended to be run once per application run. Downloads the most recent list of buildings, and schedule.
 * Public properties can be passed into other classes instead of having to manually fetch each time.
 *
 *
 */
public class OfflineCacher {
        private boolean unauth=false;
        private String uid, token;
        private NetworkInteractor ni;
        private Context Lc;

        public List<WatClass> todayClasses; // List of all classes for today
        public HashMap<String, String> buildingshm; // HashMap to look up a name from a building ID.
        public List<WatBuilding> buildings; // List of all (navigable) buildings on campus.


        public OfflineCacher(String userID, String Ltoken,NetworkInteractor lni,Context c){
           if (userID==null){
               unauth=true;
            }
            else{
               uid=userID;
               token=Ltoken;
           }
            Lc=c;
            ni=lni;
       }
       public void doCache(){
            if(!unauth){
                ni.webservice.getSchedule(uid,token, new Callback<List<WatClass>>() {
                    @Override
                    public void success(List<WatClass> watClasses, Response response) {
                            todayClasses=watClasses;
                    }

                    @Override
                    public void failure(RetrofitError error) {
                        Toast toast = Toast.makeText(Lc, "An internet connection is required! Relaunch the app when you have a connection", Toast.LENGTH_LONG);
                        toast.show();
                    }
                });
            }
           ni.webservice.buildingList(new Callback<List<WatBuilding>>() {
               @Override
               public void success(List<WatBuilding> watBuildings, Response response) {
                   buildings=watBuildings;
                   buildingshm=new HashMap<String, String>();
                   for(WatBuilding build:watBuildings ){
                       buildingshm.put(build.id,build.name);
                   }
               }

               @Override
               public void failure(RetrofitError error) {
                   Toast toast = Toast.makeText(Lc, "An internet connection is required! Relaunch the app when you have a connection", Toast.LENGTH_LONG);
                   toast.show();
               }
           });
       }
}
