package net.magmastone.NetworkInteraction;

import retrofit.RestAdapter;

/**
 * Created by alex on 8/6/15.
 */
public class NetworkInteractor {
    public WatService webservice;
    public NetworkInteractor(){
        RestAdapter rA = new RestAdapter.Builder().setEndpoint("http://ssvps.magmastone.net").build();
        webservice=rA.create(WatService.class);
    }

}
