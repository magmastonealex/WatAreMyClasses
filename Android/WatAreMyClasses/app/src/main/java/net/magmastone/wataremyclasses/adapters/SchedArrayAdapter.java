package net.magmastone.wataremyclasses.adapters;

/**
 * Created by alex on 8/10/15.
 *
 * Turns an array of WatClasses into something that a ListView can use.
 *
 * Expects a simple array of WatClasses as input.
 *
 * Should probably do am/pm stuff, but oh well.
 */

import android.content.Context;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.TextView;

import net.magmastone.NetworkInteraction.Models.WatBuilding;
import net.magmastone.NetworkInteraction.Models.WatClass;
import net.magmastone.wataremyclasses.R;

/**
 * Created by alex on 8/10/15.
 */
public class SchedArrayAdapter extends ArrayAdapter<WatClass> {
    private final Context context;
    private final WatClass[] classes;

    public  SchedArrayAdapter(Context context, WatClass[] classes){
        super(context, -1, classes);
        this.context = context;
        this.classes = classes;
    }
    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        LayoutInflater inflater = (LayoutInflater) context
                .getSystemService(Context.LAYOUT_INFLATER_SERVICE);
        View rowView = inflater.inflate(R.layout.list_buildings, parent, false);
        TextView bName = (TextView) rowView.findViewById(R.id.firstLine);
        TextView bID = (TextView) rowView.findViewById(R.id.secondLine);
        WatClass cls = classes[position];
        String clsShort = cls.class_name.split(" - ")[0];
        bName.setText(cls.type+" - "+clsShort+" - "+cls.where);
        bID.setText(cls.timestamp.split(" ")[0]+" -> "+cls.timeend.split(" ")[0]);
        return rowView;
    }
}
