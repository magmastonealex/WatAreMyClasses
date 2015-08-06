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
 */

public interface WatService {
    public interface GitHubService {
        @GET("/getnextclass")
        void getNextClass(@Query("userid") String userID, @Query("token") String userToken, Callback<WatClass> cb);

        @GET("/getschedule")
        void getSchedule(@Query("userid") String userID, @Query("token") String userToken,Callback<List<WatClass>> cb);


        @GET("/getpath")
        void getPath(@Query("node1") String nodeID1, @Query("node2") String nodeID2,Callback<List<WatNode>> cb);

        @GET("/getclosestnode")
        void getClosestNode(@Query("lat") String lat, @Query("lon") String lon,Callback<WatNode> cb);

        @GET("/buildinglist")
        void buildingList(Callback<List<WatBuilding>> cb);

    }

}
