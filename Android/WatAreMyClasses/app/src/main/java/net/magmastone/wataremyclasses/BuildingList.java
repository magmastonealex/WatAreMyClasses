package net.magmastone.wataremyclasses;

import android.content.Context;
import android.content.Intent;
import android.os.Build;
import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ListView;

import net.magmastone.NetworkInteraction.Models.WatBuilding;
import net.magmastone.wataremyclasses.adapters.BuildingArrayAdapter;

import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

/*

Very simple activity to display the list of buildings on campus, and return the ID of the selected one back.

Expects an Intent that contains an ArrayList of buildings under the key "buildings"
Will return the building node ID that was selected.
*/

public class BuildingList extends ActionBarActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_building_list);

        final ListView listview = (ListView) findViewById(R.id.listview);
        Intent intent = getIntent();
        ArrayList<WatBuilding> wb= intent.getParcelableArrayListExtra("buildings");
        Log.d("BAA", wb.get(0).name);
        final WatBuilding[] arrayWatBuilding = wb.toArray(new WatBuilding[wb.size()]);
        BuildingArrayAdapter baa = new BuildingArrayAdapter(this,arrayWatBuilding);
        listview.setAdapter(baa);
        listview.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                finishWithBuilding("b-"+arrayWatBuilding[position].id); //Turn it into a node ID
            }
        });
        }

        private void finishWithBuilding(String bID){
            Intent inte = new Intent();
            inte.putExtra("nodeID",bID);
            setResult(RESULT_OK,inte);
            finish();
        }





}
