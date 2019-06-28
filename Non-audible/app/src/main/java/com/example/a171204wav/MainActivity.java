package com.example.a171204wav;

import android.Manifest;
import android.content.pm.PackageManager;
import android.media.AudioFormat;
import android.media.AudioManager;
import android.media.AudioTrack;
import android.media.MediaPlayer;
import android.media.MediaRecorder;
import android.os.Build;
import android.os.Environment;
import android.os.Handler;
import android.support.annotation.NonNull;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

import java.io.File;
import java.io.IOException;

public class MainActivity extends AppCompatActivity {

    private final String TAG = "MainActivity";

    String sdRootPath = Environment.getExternalStorageDirectory().getAbsolutePath();
    String mFilePath;
    MediaPlayer mPlayer = null;
    Button mBtnRecord;
    Button mBtnStop;
    Button mBtnPlay;
    WavRecorder wavRecorder;


    private final int duration = 4; //sec
    private final int sampleRate = 44100;
    private final int numSamples = duration * sampleRate;
    private final double sample[] = new double[numSamples];
    private final double freq = 18000; //hz
    private final byte generatedSnd[] = new byte[2 * numSamples];

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (Build.VERSION.SDK_INT >= 23) {
            if(grantResults[0]== PackageManager.PERMISSION_GRANTED){
            }
        }
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.activity_main);
        mBtnRecord = (Button)findViewById(R.id.btnRecord);
        mBtnStop = (Button)findViewById(R.id.btnStop);
        mBtnPlay = (Button)findViewById(R.id.btnPlay);
    }

    @Override
    protected void onStart() {
        super.onStart();
        if (Build.VERSION.SDK_INT >= 23) {
            if (ContextCompat.checkSelfPermission(this, Manifest.permission.RECORD_AUDIO) == PackageManager.PERMISSION_GRANTED) {
            } else {
                ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.RECORD_AUDIO}, 2);
            }
        } else {
            Toast.makeText(this, "Record Audio Permission is Grant", Toast.LENGTH_SHORT).show();
        }
        if (Build.VERSION.SDK_INT >= 23) {
            if (checkSelfPermission(Manifest.permission.WRITE_EXTERNAL_STORAGE) == PackageManager.PERMISSION_GRANTED) {
            } else {
                ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.WRITE_EXTERNAL_STORAGE}, 1);
            }
        } else {
            Toast.makeText(this, "External Storage Permission is Grant", Toast.LENGTH_SHORT).show();
        }

        String dirPath = sdRootPath + "/jhRecord";
        File file = new File(dirPath);
        if (!file.exists()) {
            file.mkdir();
            if(!file.exists()){
                Toast.makeText(this, "Make dir Error", Toast.LENGTH_SHORT).show();
            }
        }
    }

    public void onBtnRecord() {

        mFilePath = sdRootPath + "/jhRecord/note8_20K_"+ System.currentTimeMillis() + ".wav";
        wavRecorder = new WavRecorder(mFilePath);

        genTone();
        Log.d(TAG,"Make Tone");
        playSound();
        Log.d(TAG,"Play start");
        wavRecorder.startRecording();
        Log.d(TAG,"Recorder start");
        Log.d(TAG,mFilePath);

        mBtnRecord.setEnabled(false);
        mBtnStop.setEnabled(true);
        mBtnPlay.setEnabled(false);

        Handler mHandler = new Handler();
        mHandler.postDelayed(new Runnable() {
            @Override
            public void run() {
                Log.d(TAG,"Goto Recorder stop");
                onBtnStop();
            }
        },3000);
    }

    public void onBtnStop() {
        wavRecorder.stopRecording();

        mBtnRecord.setEnabled(true);
        mBtnStop.setEnabled(false);
        mBtnPlay.setEnabled(true);
    }

    public void onBtnPlay() {
        if( mPlayer != null ) {
            mPlayer.stop();
            mPlayer.release();
            mPlayer = null;
        }
        mPlayer = new MediaPlayer();

        try {
            mPlayer.setDataSource(mFilePath);
            mPlayer.prepare();
        } catch(IOException e) {
            Log.d("tag", "Audio Play error");
            return;
        }
        mPlayer.start();
    }

    public void onClick(View v) {
        switch( v.getId() ) {
            case R.id.btnRecord :
                onBtnRecord();
                break;
            case R.id.btnStop :
                onBtnStop();
                break;
            case R.id.btnPlay :
                onBtnPlay();
                break;
        }
    }
/*
    public void onInfo(MediaRecorder mr, int what, int extra) {
        switch( what ) {
            case MediaRecorder.MEDIA_RECORDER_INFO_MAX_DURATION_REACHED :
                onBtnStop();
                break;
        }
    }
*/
    public void genTone(){
        for (int i = 0; i < numSamples; i++) {
            sample[i] = Math.sin(2*Math.PI * i / (sampleRate/freq));
        }
        int idx = 0;
        for (double dVal : sample) {
            short val = (short)(dVal * 32767);
            generatedSnd[idx++] = (byte) (val & 0x00ff);
            generatedSnd[idx++] = (byte) ((val & 0xff00) >>> 8);
        }
    }

    public void playSound(){
        AudioTrack audioTrack = new AudioTrack(AudioManager.STREAM_MUSIC, sampleRate, AudioFormat.CHANNEL_OUT_MONO, AudioFormat.ENCODING_PCM_16BIT, numSamples, AudioTrack.MODE_STREAM);
        audioTrack.write(generatedSnd,0,numSamples);
        audioTrack.play();
        audioTrack.flush();
    }
}
