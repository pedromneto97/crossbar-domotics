###############################################################################
#
# Copyright (C) 2014, Tavendo GmbH and/or collaborators. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
###############################################################################

from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp.types import SubscribeOptions
from mongoengine import connect
from os import environ
from twisted.internet.defer import inlineCallbacks
from twisted.logger import Logger

from Controllers.MeasurementController import *
from Controllers.ResidenceController import *
from Controllers.ResidenceTypeController import *
from Controllers.RoomController import *
from Controllers.RoomTypeController import *
from Controllers.SceneItemController import *
from Controllers.SceneItemTypeController import *
from Controllers.UserController import *

PREFIX = 'com.herokuapp.crossbar-pedro'


class AppSession(ApplicationSession):
    log = Logger()

    connect(host=environ['MONGODB_URI'])

    @inlineCallbacks
    def onJoin(self, details):
        """
        Users topics
        """
        yield self.register(get_user, '{}.user.id'.format(PREFIX))
        yield self.register(get_user_by_cpf, '{}.user.cpf'.format(PREFIX))
        yield self.register(insert_user, '{}.user.create'.format(PREFIX))
        yield self.register(edit_user, '{}.user.edit'.format(PREFIX))
        yield self.register(delete_user, '{}.user.delete'.format(PREFIX))
        yield self.register(get_residences, '{}.user.residences'.format(PREFIX))

        """
        Residence Topics
        """
        yield self.register(get_residence_by_alias, '{}.residence.alias'.format(PREFIX))
        yield self.register(create_residence, '{}.residence.create'.format(PREFIX))
        yield self.subscribe(edit_residence, '{}.residence..edit'.format(PREFIX), SubscribeOptions(match='wildcard'))
        yield self.subscribe(add_user_to_residence, '{}.residence..add_user'.format(PREFIX),
                             SubscribeOptions(match='wildcard'))
        yield self.register(delete_residence, '{}.residence.delete'.format(PREFIX))

        """
        Rooms topics
        """
        yield self.register(get_room_by_alias, '{}.room.alias'.format(PREFIX))
        # Uses residence ID to listen to new rooms in a residence (Only in create)
        yield self.subscribe(insert_room, '{}.room..create'.format(PREFIX), SubscribeOptions(match='wildcard'))
        yield self.subscribe(edit_room, '{}.room..edit'.format(PREFIX), SubscribeOptions(match='wildcard'))
        yield self.subscribe(delete_room, '{}.room..delete'.format(PREFIX), SubscribeOptions(match='wildcard'))

        """
        SceneItem topics
        """
        yield self.subscribe(insert_scene_item, '{}.scene_item..create'.format(PREFIX),
                             SubscribeOptions(match='wildcard'))
        yield self.subscribe(edit_scene_item, '{}.scene_item..edit'.format(PREFIX), SubscribeOptions(match='wildcard'))
        yield self.subscribe(disable_scene_item, '{}.scene_item..remove'.format(PREFIX),
                             SubscribeOptions(match='wildcard'))

        """
        Measurements
        """
        yield self.register(get_last_measurement, '{}.measurement.last'.format(PREFIX))
        yield self.subscribe(new_measurement, '{}.measurement..create'.format(PREFIX),
                             SubscribeOptions(match='wildcard'))

        """
        Residence Type Topics
        """
        yield self.register(get_residence_types, '{}.residence_type.types'.format(PREFIX))
        yield self.register(get_residence_type, '{}.residence_type.type'.format(PREFIX))
        yield self.register(create_residence_type, '{}.residence_type.create'.format(PREFIX))
        yield self.subscribe(edit_residence_type, '{}.residence_type..edit'.format(PREFIX), SubscribeOptions(match='wildcard'))
        yield self.register(remove_residence_type, '{}.residence_type.remove'.format(PREFIX))

        """
        Room Type Topics
        """
        yield self.register(get_room_types, '{}.room_type.types'.format(PREFIX))
        yield self.register(get_room_type, '{}.room_type.type'.format(PREFIX))
        yield self.register(create_room_type, '{}.room_type.create'.format(PREFIX))
        yield self.subscribe(edit_room_type, '{}.room_type..edit'.format(PREFIX), SubscribeOptions(match='wildcard'))
        yield self.register(remove_room_type, '{}.room_type.remove'.format(PREFIX))

        """
        Scene Item Type Topics
        """
        yield self.register(get_scene_item_type_by_type, '{}.scene_item_type.type'.format(PREFIX))
        yield self.register(insert_scene_item_type, '{}.scene_item_type.create'.format(PREFIX))
        yield self.subscribe(edit_scene_item_type, '{}.scene_item_type..edit'.format(PREFIX), SubscribeOptions(match='wildcard'))
        yield self.subscribe(add_pattern, '{}.scene_item_type..pattern.new'.format(PREFIX), SubscribeOptions(match='wildcard'))
        yield self.subscribe(remove_pattern, '{}.scene_item_type..pattern.remove'.format(PREFIX), SubscribeOptions(match='wildcard'))
        yield self.register(delete_scene_item_type, '{}.scene_item_type.remove'.format(PREFIX))