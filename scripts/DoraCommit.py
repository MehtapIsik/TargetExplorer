#!/usr/bin/env python
import TargetExplorer
import re
import app_master, app_stage

# sanity check on stage db - make sure each gather script has been run since the last commit
stage_version_row = app_stage.models.Version.query.first()
master_version_row = app_master.models.Version.query.first()

data_problem = False

for data_type in ['uniprot']:
    datestamp_type = data_type+'_datestamp'
    stage_datestamp = getattr(stage_version_row, datestamp_type)
    master_datestamp = getattr(master_version_row, datestamp_type)
    # print stage_datestamp , master_datestamp
    # print stage_datestamp > master_datestamp
    # print stage_datestamp < master_datestamp
    # print stage_datestamp == master_datestamp
    if stage_datestamp == None:
        print 'data_type "%s" FAIL: no data in stage db' % data_type
        data_problem = True
    elif master_datestamp == None:
        print 'data_type "%s" PASS: no data in master db, but present in stage db (%s)' % (data_type, stage_datestamp.strftime(TargetExplorer.core.datestamp_format_string))
    elif stage_datestamp <= master_datestamp:
        print 'data_type "%s" FAIL: staged data (%s) is older than or as old as master (%s)' % (data_type, stage_datestamp.strftime(TargetExplorer.core.datestamp_format_string), master_datestamp.strftime(TargetExplorer.core.datestamp_format_string))
        data_problem = True
    elif stage_datestamp > master_datestamp:
        print 'data_type "%s" PASS: staged data (%s) is newer than master (%s)' % (data_type, stage_datestamp.strftime(TargetExplorer.core.datestamp_format_string), master_datestamp.strftime(TargetExplorer.core.datestamp_format_string))

if data_problem:
    raise Exception, 'Commit aborted.'
else:
    print 'Proceeding to commit to master db...'

# read previous master db version_id
old_version_id = master_version_row.version_id

# drop existing data in master db
app_master.db.drop_all()
app_master.db.create_all()

# copy data from stage db to master db
for table_name in app_stage.models.table_class_names:
    stage_table = getattr(app_stage.models, table_name)
    stage_rows = stage_table.query.all()
    for stage_row in stage_rows:
        app_master.db.session.merge(stage_row)

# write master db to disk
app_master.db.session.commit()

# iterate version id
new_version_id = old_version_id + 1
master_version_row = app_master.models.Version.query.first()
master_version_row.version_id = new_version_id

# write master db with updated version id
app_master.db.session.commit()

print 'Upgraded master db from version %d to %d' % (old_version_id, new_version_id)
print 'Done.'
