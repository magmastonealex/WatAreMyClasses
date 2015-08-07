package net.magmastone.NetworkInteraction.Models;

import org.parceler.Parcel;

/**
 * Created by alex on 8/6/15.
 *
 * This represents a single class returned by the API.
 */
@Parcel
public class WatClass {
    public  int id;
    public String class_name;
    public String section;
    public  String timestamp;
    public String timeend;
    public String instructor;
    public  String type;
    public  String where;
}
