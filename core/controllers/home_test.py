# Copyright 2014 The Oppia Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests for the home page (i.e. the splash page and user dashboard)."""

__author__ = 'Sean Lip'

from core.domain import rights_manager
from core.tests import test_utils


class HomePageTest(test_utils.GenericTestBase):

    def test_logged_out_homepage(self):
        """Test the logged-out version of the home page."""
        response = self.testapp.get('/')
        self.assertEqual(response.status_int, 200)
        response.mustcontain(
            'Bite-sized learning journeys',
            'View Gallery', '100% Free',
            'Learn', 'About', 'Contact', 'Login', 'Contribute',
            # No navbar tabs should be highlighted.
            no=['class="active"',
                'Profile', 'Logout', 'Create an exploration', 'Dashboard'])

    def test_logged_in_but_not_registered_as_editor_homepage(self):
        """Test the logged-in-but-not-editor version of the home page."""
        response = self.testapp.get('/')
        self.assertEqual(response.status_int, 200)
        response.mustcontain(
            'Login', self.get_expected_login_url('/'),
            no=['Logout', self.get_expected_logout_url('/')])

        self.login('reader@example.com')
        response = self.testapp.get('/')
        self.assertEqual(response.status_int, 200)
        response.mustcontain(
            'Bite-sized learning journeys',
            'Contribute', 'Profile', 'Logout', 'Create Exploration',
            self.get_expected_logout_url('/'),
            no=['Login', 'Create an Oppia account', 'Dashboard',
                self.get_expected_login_url('/')])
        self.logout()

    def test_logged_in_and_registered_as_editor_homepage(self):
        """Test the logged-in-and-editor home page (the 'dashboard')."""
        response = self.testapp.get('/')
        self.assertEqual(response.status_int, 200)
        response.mustcontain(
            'Login', self.get_expected_login_url('/'),
            no=['Logout', self.get_expected_logout_url('/')])

        self.register_editor('editor@example.com')
        self.login('editor@example.com')

        response = self.testapp.get('/')
        self.assertEqual(response.status_int, 200)
        response.mustcontain(
            'Dashboard', 'Contribute', 'Profile', 'Logout',
            self.get_expected_logout_url('/'),
            no=['Login', 'Create an Oppia account',
                'Bite-sized learning journeys',
                self.get_expected_login_url('/')])
        self.logout()


class DashboardHandlerTest(test_utils.GenericTestBase):

    OWNER_EMAIL = 'editor@example.com'
    COLLABORATOR_EMAIL = 'collaborator@example.com'
    VIEWER_EMAIL = 'viewer@example.com'
    EXP_ID = 'exp_id'
    EXP_TITLE = 'Exploration title'

    def setUp(self):
        super(DashboardHandlerTest, self).setUp()
        self.register_editor(self.OWNER_EMAIL, username='owner')
        self.register_editor(
            self.COLLABORATOR_EMAIL, username='collaborator')
        self.register_editor(self.VIEWER_EMAIL, username='viewer')
        self.OWNER_ID = self.get_user_id_from_email(self.OWNER_EMAIL)
        self.COLLABORATOR_ID = self.get_user_id_from_email(
            self.COLLABORATOR_EMAIL)
        self.VIEWER_ID = self.get_user_id_from_email(self.VIEWER_EMAIL)

    def test_no_explorations(self):
        self.login(self.OWNER_EMAIL)
        response = self.get_json('/dashboardhandler/data')
        self.assertEqual(response['explorations'], {})
        self.logout()

    def test_managers_can_see_explorations_on_dashboard(self):
        self.save_new_default_exploration(
            self.EXP_ID, self.OWNER_ID, title=self.EXP_TITLE)
        self.set_admins([self.OWNER_EMAIL])

        self.login(self.OWNER_EMAIL)
        response = self.get_json('/dashboardhandler/data')
        self.assertEqual(len(response['explorations']), 1)
        self.assertIn(self.EXP_ID, response['explorations'])
        self.assertEqual(
            response['explorations'][self.EXP_ID]['rights']['status'],
            rights_manager.EXPLORATION_STATUS_PRIVATE)

        rights_manager.publish_exploration(self.OWNER_ID, self.EXP_ID)
        response = self.get_json('/dashboardhandler/data')
        self.assertEqual(len(response['explorations']), 1)
        self.assertIn(self.EXP_ID, response['explorations'])
        self.assertEqual(
            response['explorations'][self.EXP_ID]['rights']['status'],
            rights_manager.EXPLORATION_STATUS_PUBLIC)

        rights_manager.publicize_exploration(self.OWNER_ID, self.EXP_ID)
        response = self.get_json('/dashboardhandler/data')
        self.assertEqual(len(response['explorations']), 1)
        self.assertIn(self.EXP_ID, response['explorations'])
        self.assertEqual(
            response['explorations'][self.EXP_ID]['rights']['status'],
            rights_manager.EXPLORATION_STATUS_PUBLICIZED)
        self.logout()

    def test_collaborators_can_see_explorations_on_dashboard(self):
        self.save_new_default_exploration(
            self.EXP_ID, self.OWNER_ID, title=self.EXP_TITLE)
        rights_manager.assign_role(
            self.OWNER_ID, self.EXP_ID, self.COLLABORATOR_ID,
            rights_manager.ROLE_EDITOR)
        self.set_admins([self.OWNER_EMAIL])

        self.login(self.COLLABORATOR_EMAIL)
        response = self.get_json('/dashboardhandler/data')
        self.assertEqual(len(response['explorations']), 1)
        self.assertIn(self.EXP_ID, response['explorations'])
        self.assertEqual(
            response['explorations'][self.EXP_ID]['rights']['status'],
            rights_manager.EXPLORATION_STATUS_PRIVATE)

        rights_manager.publish_exploration(self.OWNER_ID, self.EXP_ID)
        response = self.get_json('/dashboardhandler/data')
        self.assertEqual(len(response['explorations']), 1)
        self.assertIn(self.EXP_ID, response['explorations'])
        self.assertEqual(
            response['explorations'][self.EXP_ID]['rights']['status'],
            rights_manager.EXPLORATION_STATUS_PUBLIC)

        rights_manager.publicize_exploration(self.OWNER_ID, self.EXP_ID)
        response = self.get_json('/dashboardhandler/data')
        self.assertEqual(len(response['explorations']), 1)
        self.assertIn(self.EXP_ID, response['explorations'])
        self.assertEqual(
            response['explorations'][self.EXP_ID]['rights']['status'],
            rights_manager.EXPLORATION_STATUS_PUBLICIZED)

        self.logout()

    def test_viewer_cannot_see_explorations_on_dashboard(self):
        self.save_new_default_exploration(
            self.EXP_ID, self.OWNER_ID, title=self.EXP_TITLE)
        rights_manager.assign_role(
            self.OWNER_ID, self.EXP_ID, self.VIEWER_ID,
            rights_manager.ROLE_VIEWER)

        self.login(self.VIEWER_EMAIL)
        response = self.get_json('/dashboardhandler/data')
        self.assertEqual(response['explorations'], {})

        rights_manager.publish_exploration(self.OWNER_ID, self.EXP_ID)
        response = self.get_json('/dashboardhandler/data')
        self.assertEqual(response['explorations'], {})

        self.set_admins([self.OWNER_EMAIL])
        rights_manager.publicize_exploration(self.OWNER_ID, self.EXP_ID)
        response = self.get_json('/dashboardhandler/data')
        self.assertEqual(response['explorations'], {})
        self.logout()
