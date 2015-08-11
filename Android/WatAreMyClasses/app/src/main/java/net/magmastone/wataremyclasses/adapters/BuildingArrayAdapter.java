package net.magmastone.wataremyclasses.adapters;

import android.content.Context;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ImageView;
import android.widget.TextView;

import net.magmastone.NetworkInteraction.Models.WatBuilding;
import net.magmastone.wataremyclasses.R;

/**
 * Created by alex on 8/10/15.
 */
public class BuildingArrayAdapter extends ArrayAdapter<WatBuilding> {
    private final Context context;
    private final WatBuilding[] buildings;

    public BuildingArrayAdapter(Context context, WatBuilding[] buildings){

        super(context, -1, buildings);
        Log.d("BAA", buildings[0].name);
        this.context = context;
        this.buildings = buildings;
    }
    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        LayoutInflater inflater = (LayoutInflater) context
                .getSystemService(Context.LAYOUT_INFLATER_SERVICE);
        View rowView = inflater.inflate(R.layout.list_buildings, parent, false);
        TextView bName = (TextView) rowView.findViewById(R.id.firstLine);
        TextView bID = (TextView) rowView.findViewById(R.id.secondLine);
        WatBuilding build = buildings[position];
        bName.setText(build.name);
        bID.setText(build.id);
        return rowView;
    }
}
