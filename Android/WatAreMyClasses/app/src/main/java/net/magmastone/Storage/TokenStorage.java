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

            String uid = sP.getString("uid","baduserid");
            if(uid.equals("baduserid")){
                return  null;
            }else{
                return  uid;
            }
        }
        public String getToken(){

            String tkn = sP.getString("token","badtoken");
            if(tkn.equals("badtoken")){
                return  null;
            }else{
                return  tkn;
            }
        }
        public Boolean hasLoggedIn(){

               if(sP.getString("token","nope").equals("nope")){
                   return false;
               }else{
                   return true;
               }

        }

}
