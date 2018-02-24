wrfconf
=======

A commandline tool for generating WRF configuration from structured YAML files.

The purpose of this package is to be able to easily generate WRF and WPS namelists in an extensible manner. Namelists are generated from configuration
files which can be source controlled and include additional metadata not present in the namelist

Quick start
============

wrfconf can be installed using pip:

::

    pip install wrfconf

Before the WRF and WPS namelists can be generated, a yaml file describing the time, domain and physics settings. This can be generated using python or
other scripting language or manually edited. An example YAML file is included in examples/run.yml:

::

    ---
    meta:
      owner: Jared Lewis
      email: jared@jared.kiwi.nz
      run_name: test

    run_info:
      start_date: '2006-08-16_12:00:00'
      run_hours: 36
      max_dom: 2

    domain:
      parent_id: [1, 1]
      parent_grid_ratio: 1, 3,
      i_parent_start: 1, 34,
      j_parent_start: 1, 25,
      e_we: [ 85, 73]
      e_sn: [ 93, 79]
      dx: [36000, 12000]
      dy: [36000, 12000]
      map_proj: 'lambert'
      ref_lat: -41.276
      ref_lon: 169.228
      ref_x: 42.5
      ref_y: 46.5
      truelat1: -41.276
      truelat2: -41.276
      stand_lon: 169.228
      geog_data_res: ['10m','2m']

    wps:
      share:
        wrf_core: ARW
        interval_seconds: 10800
        io_form_geogrid: 2

      geogrid:
        geog_data_path: '/mnt/data/WRF/WPS_GEOG'
        opt_geogrid_tbl_path: 'geogrid/'

      ungrib:
       out_format: 'WPS'
       prefix: 'FILE'

      metgrid:
       fg_name: 'FILE'
       io_form_metgrid: 2

    wrf:
      time_control:
        interval_seconds: 10800
        input_from_file: [True, True, True, True]
        history_interval: [ 60, 60, 60, 60]
        frames_per_outfile: [ 1000, 1000, 1000, 1000]
        restart: False,
        restart_interval: 5000,
        io_form_history: 2
        io_form_restart: 2
        io_form_input: 2
        io_form_boundary: 2
        debug_level: 0

      domains:
        time_step: 180
        time_step_fract_num: 0
        time_step_fract_den: 1
        p_top_requested: 5000
        num_metgrid_levels: 32
        num_metgrid_soil_levels: 4
        feedback: 1
        smooth_option: 0


      physics:
        mp_physics:         [ 3, 3, 3, 3]
        ra_lw_physics:      [ 1, 1, 1, 1]
        ra_sw_physics:      [ 1, 1, 1, 1]
        radt:               [ 30, 30, 30, 30]
        sf_sfclay_physics:  [ 1, 1, 1, 1]
        sf_surface_physics: [ 2, 2, 2, 2]
        bl_pbl_physics:     [ 1, 1, 1, 1]
        bldt:               [ 0, 0, 0, 0]
        cu_physics:         [ 1, 1, 0, 0]
        cudt:               [ 5, 5, 5, 5]
        isfflx: 1,
        ifsnow: 1,
        icloud: 1,
        surface_input_source: 3,
        num_soil_layers:    4
        num_land_cat:       21
        sf_urban_physics:   [ 0, 0, 0, 0]

      dynamics:
        w_damping: 0,
        diff_opt: [ 1, 1, 1, 1]
        km_opt: [ 4, 4, 4, 4]
        diff_6th_opt: [ 0, 0, 0, 0]
        diff_6th_factor: 0.12, 0.12, 0.12, 0.12
        base_temp: 290.
        damp_opt: 0,
        zdamp: [5000., 5000., 5000., 5000.]
        dampcoef: [0.2, 0.2, 0.2, 0.2]
        khdif: [ 0, 0, 0, 0]
        kvdif: [ 0, 0, 0, 0]
        non_hydrostatic: [ True, True, True, True]
        moist_adv_opt: [ 1, 1, 1, 1]
        scalar_adv_opt: [ 1, 1, 1, 0]

      bdy_control:
        spec_bdy_width: 5,
        spec_zone: 1,
        relax_zone: 4,
        specified: [True, False,False,False]
        nested: [False, True, True,True]

      namelist_quilt:
        nio_tasks_per_group: 0,
        nio_groups: 1,

There are a number of top level keys in these configuration files:

meta
----

This section includes metadata about the run and does not impact the generated namelists. Any valid YAML can be included in this section

run_info
--------

Information specific to this particular run, such as the start time and length of run

domain
------

Domain specific information

wps
---

Override any attributes in the WPS file. This section follows the same structure and naming conventions as in a WPS file

wrf
---

Override any attributes in the WRF namelist. This section follows the same structure and naming conventions as in a WRF namelist file

Development setup
==================

::

    git clone https://github.com/lewisjared/wrfconf.git
    cd wrfconf
    python setup.py develop
