from unittest import TestCase

from wrfconf.conf.parse_namelist import ConfigItem, get_next_item


class TestGetNextItem(TestCase):

    def get_lines(self, t):
        lines = t.split('\n')
        return [l + '\n' for l in lines]

    def test_basic(self):
        lines = self.get_lines(""" end_day (max_dom)                   = 12,	; two digit day of ending time
 end_hour (max_dom)                  = 12,	; two digit hour of ending time
 end_minute (max_dom)                = 00,	; two digit minute of ending time""")
        self.assertEqual(get_next_item(lines), 'end_day (max_dom)                   = 12,	; two digit day of ending time')

    def test_basic_2(self):
        lines = self.get_lines(""" end_second (max_dom)                = 00,	; two digit second of ending time
                                                  It also controls when the nest domain integrations end
                                                  All start and end times are used by real.exe.

                                                  Note that one may use either run_days/run_hours etc. or 
                                                  end_year/month/day/hour etc. to control the length of 
                                                  model integration. But run_days/run_hours
                                                  takes precedence over the end times. 
                                                  Program real.exe uses start and end times only.

 interval_seconds                    = 10800,	; time interval between incoming real data, which will be the interval
                                                  between the lateral boundary condition file
 input_from_file (max_dom)           = T,       ; whether nested run will have input files for domains other than 1
 fine_input_stream (max_dom)         = 0,       ; field selection from nest input for its initialization
                                                  0: all fields are used; 2: only static and time-varying, masked land 
                                                  surface fields are used. In V3.2, this requires the use of 
                                                  io_form_auxinput2""")
        self.assertEqual(get_next_item(lines), """end_second (max_dom)                = 00,	; two digit second of ending time
                                                  It also controls when the nest domain integrations end
                                                  All start and end times are used by real.exe.""")

    def test_basic_3(self):
        lines = self.get_lines(""" cycling                             = F,       ; whether this run is a cycling run, if so, initializes look-up table for Thompson schemes only
 restart_interval		     = 1440,	; restart output file interval in minutes
 reset_simulation_start              = F,       ; whether to overwrite simulation_start_date with forecast start time
 io_form_history                     = 2,       ; 2 = netCDF """)
        self.assertEqual(get_next_item(lines), 'cycling                             = F,       ; whether this run is a cycling run, if so, initializes look-up table for Thompson schemes only')

    def test_advanced(self):
        lines = self.get_lines("""For additional regional climate surface fields

 output_diagnostics                  = 1        ; adds 36 surface diagnostic arrays (max/min/mean/std)
 auxhist3_outname                    = 'wrfxtrm_d<domain>_<date>' ; file name for added diagnostics
 io_form_auxhist3                    = 2        ; netcdf
 auxhist3_interval                   = 1440     ; minutes between outputs (1440 gives daily max/min)
 frames_per_auxhist3                 = 1        ; output times per file
                                                  Note: do restart only at multiple of auxhist3_intervals

For observation nudging:
 auxinput11_interval                 = 10       ; interval in minutes for observation data. It should be 
                                                  set as or more frequently as obs_ionf (with unit of 
                                                  coarse domain time step).
 auxinput11_end_h                    = 6        ; end of observation time in hours""")
        self.assertEqual(get_next_item(lines), """output_diagnostics                  = 1        ; adds 36 surface diagnostic arrays (max/min/mean/std)""")


class TestConfigItem(TestCase):
    def test_basic_parse(self):
        i = ConfigItem(' time_step_fract_num                 = 0,	; numerator for fractional time step\n')
        self.assertFalse(i.is_section)
        self.assertEqual(i.name, 'time_step_fract_num')
        self.assertEqual(i.default, '0')
        self.assertEqual(i.description, 'numerator for fractional time step')

    def test_multiline(self):
        i = ConfigItem(" e_vert (max_dom)                    = 30,	; end index in z (vertical) direction (staggered dimension)\n                                                  Note: this refers to full levels including surface and top\n                                                  vertical dimensions need to be the same for all nests\n                                                  Note: most variables are unstaggered (= staggered dim - 1)\n")
        self.assertFalse(i.is_section)
        self.assertEqual(i.name, 'e_vert')
        self.assertTrue(i.is_multi_dim)
        self.assertEqual(i.default, '30')
        self.assertEqual(i.description, 'end index in z (vertical) direction (staggered dimension)\nNote: this refers to full levels including surface and top\nvertical dimensions need to be the same for all nests\nNote: most variables are unstaggered (= staggered dim - 1)')