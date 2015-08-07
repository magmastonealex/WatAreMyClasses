package net.magmastone.NetworkInteraction;

import net.magmastone.NetworkInteraction.Models.WatBuilding;
import net.magmastone.NetworkInteraction.Models.WatClass;
import net.magmastone.NetworkInteraction.Models.WatNode;

import java.util.List;

import retrofit.Callback;
import retrofit.http.GET;
import retrofit.http.Path;
import retrofit.http.Query;

/**
 * Created by alex on 8/6/15.
 *
 * This is the basic API implementation definition as required by Retrofit.
 *
 * Parameters and usage is identical to what's specified in docs/API.md. Contains a cross-platform overview.
 *
 *
 *
 */

public interface WatService {

        @GET("/getnextclass")
        void getNextClass(@Query("userid") String userID, @Query("token") String userToken, Callback<WatClass> cb); // Gets a given user's next class. Need both userID and token as taken from the barcode.

        @GET("/getschedule")
        void getSchedule(@Query("userid") String userID, @Query("token") String userToken,Callback<List<WatClass>> cb); // Gets a given user's entire day's schedule. Need both userID and token as taken from the barcode.


        @GET("/getpath")
        void getPath(@Query("node1") String nodeID1, @Query("node2") String nodeID2,Callback<List<WatNode>> cb); // Gets a path between two nodes. Requires no auth.

        @GET("/getclosestnode")
        void getClosestNode(@Query("lat") String lat, @Query("lon") String lon,Callback<WatNode> cb); // Gets the closest known node to the user. Requires no auth.

        @GET("/buildinglist")
        void buildingList(Callback<List<WatBuilding>> cb); // Gets all buildings on campus. SHOULD BE CACHED! Requires no auth.


}
