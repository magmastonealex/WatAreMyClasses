package net.magmastone.NetworkInteraction.Models;

import android.os.Parcel;
import android.os.Parcelable;

/**
 * Created by alex on 8/6/15.
 *
 * This represents a single building as returned by the API.
 */
public class WatBuilding implements Parcelable{
    public  String name;
    public  String id;

    protected WatBuilding(Parcel in) {
        name = in.readString();
        id = in.readString();
    }

    @Override
    public int describeContents() {
        return 0;
    }

    @Override
    public void writeToParcel(Parcel dest, int flags) {
        dest.writeString(name);
        dest.writeString(id);
    }

    @SuppressWarnings("unused")
    public static final Parcelable.Creator<WatBuilding> CREATOR = new Parcelable.Creator<WatBuilding>() {
        @Override
        public WatBuilding createFromParcel(Parcel in) {
            return new WatBuilding(in);
        }

        @Override
        public WatBuilding[] newArray(int size) {
            return new WatBuilding[size];
        }
    };

}
