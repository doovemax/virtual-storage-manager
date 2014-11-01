# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2014 Intel Inc.
# All Rights Reserved.

# Licensed under the Apache License, Version 2.0 (the"License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#  http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the
# specific language governing permissions and limitations
# under the License.

# -*- encoding: utf-8 -*-
#
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from migrate import ForeignKeyConstraint
from sqlalchemy import MetaData, Table
from sqlalchemy.sql.expression import select

from vsm.db.sqlalchemy import utils

def upgrade(migrate_engine):
    if migrate_engine.name == 'sqlite':
        return
    meta = MetaData(bind=migrate_engine)
    storage_pools = Table('storage_pools', meta, autoload=True)
    storage_groups = Table('storage_groups', meta, autoload=True)
    params = {'columns': [storage_pools.c.primary_storage_group_id],
              'refcolumns': [storage_groups.c.id]}
    if migrate_engine.name == 'mysql':
        params['name'] = "_".join(('storage_pools', 'primary_storage_group_ids', 'fkey'))
    fkey = ForeignKeyConstraint(**params)
    fkey.create()

def downgrade(migrate_engine):
    if migrate_engine.name == 'sqlite':
        return
    meta = MetaData(bind=migrate_engine)
    storage_pools = Table('storage_pools', meta, autoload=True)
    storage_groups = Table('storage_groups', meta, autolaod=True)
    params = {'columns': [storage_pools.c.primary_storage_group_id],
              'refcolumns': [storage_groups.c.id]}
    fkey = ForeignKeyConstraint(**params)
    fkey.drop()                        