package net.magmastone.wataremyclasses;

import android.content.Context;
import android.content.Intent;
import android.os.Build;
import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.ArrayAdapter;
import android.widget.ListView;

import net.magmastone.NetworkInteraction.Models.WatBuilding;
import net.magmastone.wataremyclasses.adapters.BuildingArrayAdapter;

import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;


public class BuildingList extends ActionBarActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_building_list);

        final ListView listview = (ListView) findViewById(R.id.listview);
        Intent intent = getIntent();
        ArrayList<WatBuilding> wb= intent.getParcelableArrayListExtra("buildings");
        Log.d("BAA", wb.get(0).name);
        WatBuilding[] arrayWatBuilding = wb.toArray(new WatBuilding[wb.size()]);
        BuildingArrayAdapter baa = new BuildingArrayAdapter(this,arrayWatBuilding);
        listview.setAdapter(baa);

    }


}
