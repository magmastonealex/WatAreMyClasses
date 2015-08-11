package net.magmastone.NetworkInteraction.Models;

import android.os.Parcelable;

import android.os.Parcel;

/**
 * Created by alex on 8/6/15.
 *
 * This represents a single class returned by the API.
 */

public class WatClass implements Parcelable {
    public  int id;
    public String class_name;
    public String section;
    public  String timestamp;
    public String timeend;
    public String instructor;
    public  String type;
    public  String where;

    protected WatClass(Parcel in) {

        id = in.readInt();
        class_name = in.readString();
        section = in.readString();
        timestamp = in.readString();
        timeend = in.readString();
        instructor = in.readString();
        type = in.readString();
        where = in.readString();
    }

    @Override
    public int describeContents() {
        return 0;
    }

    @Override
    public void writeToParcel(Parcel dest, int flags) {
        dest.writeInt(id);
        dest.writeString(class_name);
        dest.writeString(section);
        dest.writeString(timestamp);
        dest.writeString(timeend);
        dest.writeString(instructor);
        dest.writeString(type);
        dest.writeString(where);
    }

    @SuppressWarnings("unused")
    public static final Parcelable.Creator<WatClass> CREATOR = new Parcelable.Creator<WatClass>() {
        @Override
        public WatClass createFromParcel(Parcel in) {
            return new WatClass(in);
        }

        @Override
        public WatClass[] newArray(int size) {
            return new WatClass[size];
        }
    };
}
