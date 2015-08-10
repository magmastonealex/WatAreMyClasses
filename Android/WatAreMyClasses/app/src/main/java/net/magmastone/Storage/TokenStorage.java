package net.magmastone.Storage;

import android.content.Context;
import android.content.SharedPreferences;

/**
 * Created by alex on 8/8/15.
 *
 * Storage for tokens & userIDs.
 *
 * Usage:
 *
 * tS = new TokenStorage(getActivity());
 *
 * if(tS.hasLoggedIn()){
 *     String uid = tS,getUserID();
 *     String token = tS.getToken();
 * }else{
 *     tS.setToken("hello","token");
 * }
 */
public class TokenStorage {
       private SharedPreferences sP;
       public TokenStorage(Context c){
           sP=c.getSharedPreferences("net.magmastone.wataremyclasses.TOKEN",Context.MODE_PRIVATE);
        }
        public void setToken(String userid, String token){
            SharedPreferences.Editor e = sP.edit();

            e.putString("uid",userid);
            e.putString("token",token);
            e.commit();
        }
        public String getUserID(){
            return sP.getString("uid","baduserid");
        }
        public String getToken(){
            return sP.getString("token","badtoken");
        }
        public Boolean hasLoggedIn(){
               if(sP.getString("token","nope").equals("nope")){
                   return false;
               }else{
                   return true;
               }

        }

}
