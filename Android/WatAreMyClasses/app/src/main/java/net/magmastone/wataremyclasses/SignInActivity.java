package net.magmastone.wataremyclasses;

import android.app.Activity;
import android.content.Intent;
import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import com.google.zxing.integration.android.IntentIntegrator;
import com.google.zxing.integration.android.IntentResult;

import net.magmastone.NetworkInteraction.Models.WatNode;
import net.magmastone.NetworkInteraction.NetworkInteractor;
import net.magmastone.Storage.TokenStorage;

import retrofit.Callback;
import retrofit.RetrofitError;
import retrofit.client.Response;

/*
Simple QR signin activity.

Need to style, remove TextViews, and add some functionality to the Skip button.

Handles scanning a QR code (should probably be abstracted away), storing it using TokenStorage, and moving the user on.

Moves user over to MapActivity.

 */
public class SignInActivity extends ActionBarActivity {
    private Activity ourActivity;
    private NetworkInteractor ni;
    private TextView helloTextView;
    private TokenStorage tS;
    @Override
    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        ourActivity=this; //Saved for button calbacks.
        setContentView(R.layout.activity_sign_in); // Set our view as defined in XML.
        tS = new TokenStorage(this);
        if(tS.hasLoggedIn()){
            startActivity(new Intent(this, MapActivity.class));
            finish();
        }

        //Get the required elements to make our view interactive
        Button btn = (Button) findViewById(R.id.scanButton); // Scan button to scan a barcode.
        btn.setOnClickListener(new HandleClick()); // Listener down below.

        helloTextView=(TextView) findViewById(R.id.hellotext); //Our Hello World text. Very temporary.

        ni = new NetworkInteractor(); // Example of using NetworkInteractor.
        ni.webservice.getClosestNode("43.726733","-79.781998",new Callback<WatNode>() {
            @Override
            public void success(WatNode watNode, Response response) {
                helloTextView.setText(watNode.id);
            }

            @Override
            public void failure(RetrofitError error) {
                helloTextView.setText(error.getLocalizedMessage());
            }
        });
    }


    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_sign_in, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }


    private class HandleClick implements View.OnClickListener {
        public void onClick(View btn) {
            IntentIntegrator.initiateScan(ourActivity); // This is a Zxing method.
        }
    }

    public void onActivityResult(int requestCode, int resultCode, Intent intent) {
            TextView tvUserID=(TextView)findViewById(R.id.uid);
            IntentResult scanResult = IntentIntegrator.parseActivityResult(requestCode, resultCode, intent); // Check if it's from Zxing or our own...
            if (scanResult != null) {
                String res= scanResult.getContents(); // Set the UserID text to the barcode contents.
                String[] uidtoken=res.split(":");
                tS.setToken(uidtoken[0],uidtoken[1]);
                Log.d("SignInActivity","User logged in with token: "+uidtoken[0]+":"+uidtoken[1]);
                startActivity(new Intent(this, MapActivity.class));
                finish();
            }
    }

}
