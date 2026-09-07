package com.faa.fcbclip;

import android.app.Activity;
import android.os.Bundle;
import android.widget.TextView;

/**
 * Dibuka SEKALI setelah install agar aplikasi keluar dari stopped-state
 * (syarat broadcast ADB diterima). Setelah itu tidak perlu dibuka lagi.
 */
public class MainActivity extends Activity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        TextView tv = new TextView(this);
        tv.setText("FCB Helper aktif.\n\nAplikasi ini tidak punya tampilan. "
                + "Cukup dibuka sekali agar broadcast ADB jalan, "
                + "setelah itu tidak perlu dibuka lagi.\n\n"
                + "Keyboard utama (GBoard) tidak berubah sama sekali.");
        tv.setTextSize(18);
        tv.setPadding(40, 40, 40, 40);
        setContentView(tv);
    }
}
