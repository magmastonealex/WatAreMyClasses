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
import net.magmastone.NetworkInteraction.Models.WatClass;
import net.magmastone.wataremyclasses.adapters.BuildingArrayAdapter;
import net.magmastone.wataremyclasses.adapters.SchedArrayAdapter;

import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;


public class ScheduleViewActivity extends ActionBarActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_building_list);

        final ListView listview = (ListView) findViewById(R.id.listview);
        Intent intent = getIntent();
        ArrayList<WatClass> wb= intent.getParcelableArrayListExtra("classes");
        Log.d("BAA", wb.get(0).class_name);
        final WatClass[] arrayWatClass = wb.toArray(new WatClass[wb.size()]);
        SchedArrayAdapter baa = new SchedArrayAdapter(this,arrayWatClass);
        listview.setAdapter(baa);
        listview.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                String loc=arrayWatClass[position].where.split(" ")[0];
                finishWithBuilding("b-"+loc); //Turn it into a node ID
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
