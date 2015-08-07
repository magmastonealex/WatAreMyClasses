package net.magmastone.NetworkInteraction;

import retrofit.RestAdapter;

/**
 * Created by alex on 8/6/15.
 *
 * This is a basic class to allow access to the webservice.
 *
 * Usage boils down to:
 *
 * ni= new NetworkInteractor()
 *
 * ni.webservice.yourmethod() - remember the Callback here! Android Studio/Eclipse will autocomplete a basic version.
 *
 */
public class NetworkInteractor {
    public WatService webservice;
    public NetworkInteractor(){
        RestAdapter rA = new RestAdapter.Builder().setEndpoint("http://ssvps.magmastone.net").build();
        webservice=rA.create(WatService.class);
    }

}
