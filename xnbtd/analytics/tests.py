import csv
from io import StringIO

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Expense
from xnbtd.analytics.export import export_as_csv


class ExpenseModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.expense = Expense.objects.create(
            title='Test Expense',
            license_plate='abc123',
            amount=100.50,
            date='2023-01-01',
            linked_user=self.user
        )

    def test_expense_creation(self):
        """Test the expense model creation and string representation"""
        self.assertEqual(self.expense.title, 'Test Expense')
        self.assertEqual(self.expense.license_plate, 'ABC123')  # Should be uppercase
        self.assertEqual(self.expense.amount, 100.50)
        self.assertTrue(isinstance(self.expense, Expense))
        self.assertTrue('Test Expense' in str(self.expense))
        self.assertTrue('ABC123' in str(self.expense))


class ExpenseAdminTest(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpassword'
        )
        self.client.login(username='admin', password='adminpassword')

        # Create some test expenses
        Expense.objects.create(
            title='Expense 1',
            license_plate='abc123',
            amount=100.50,
            date='2023-01-01',
            linked_user=self.admin_user
        )
        Expense.objects.create(
            title='Expense 2',
            license_plate='def456',
            amount=200.75,
            date='2023-01-02',
            linked_user=self.admin_user
        )

    def test_expense_admin_list(self):
        """Test the expense admin list view"""
        url = reverse('admin:analytics_expense_changelist')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Expense 1')
        self.assertContains(response, 'Expense 2')
        self.assertContains(response, 'ABC123')
        self.assertContains(response, 'DEF456')

    def test_expense_admin_add(self):
        """Test adding an expense through the admin"""
        url = reverse('admin:analytics_expense_add')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Test POST to create a new expense
        post_data = {
            'title': 'New Expense',
            'license_plate': 'ghi789',
            'amount': '300.25',
            'date': '2023-01-03',
            'linked_user': self.admin_user.id,
        }
        response = self.client.post(url, post_data, follow=True)
        self.assertEqual(response.status_code, 200)

        # Verify the expense was created
        self.assertTrue(Expense.objects.filter(title='New Expense').exists())
        expense = Expense.objects.get(title='New Expense')
        self.assertEqual(expense.license_plate, 'GHI789')  # Should be uppercase
        self.assertEqual(float(expense.amount), 300.25)


class ExportCSVTest(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpassword'
        )
        self.client.login(username='admin', password='adminpassword')

        # Create some test expenses
        self.expense1 = Expense.objects.create(
            title='Expense 1',
            license_plate='abc123',
            amount=100.50,
            date='2023-01-01',
            linked_user=self.admin_user
        )
        self.expense2 = Expense.objects.create(
            title='Expense 2',
            license_plate='def456',
            amount=200.75,
            date='2023-01-02',
            linked_user=self.admin_user
        )

    def test_export_as_csv_function(self):
        """Test the export_as_csv function directly"""
        from django.contrib.admin.sites import AdminSite
        from django.http import HttpRequest
        from xnbtd.analytics.admin import ExpenseAdmin

        # Create a mock request
        request = HttpRequest()
        request.user = self.admin_user

        # Create a model admin instance
        model_admin = ExpenseAdmin(Expense, AdminSite())

        # Get all expenses
        queryset = Expense.objects.all()

        # Call the export function
        response = export_as_csv(model_admin, request, queryset)

        # Check the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertTrue('attachment; filename=' in response['Content-Disposition'])

        # Parse the CSV content
        content = response.content.decode('utf-8')
        csv_reader = csv.reader(StringIO(content))
        rows = list(csv_reader)

        # Check the header row
        self.assertTrue('Intitulé' in rows[0])
        self.assertTrue("Plaque d'immatriculation" in rows[0] or "license_plate" in rows[0])
        self.assertTrue('Montant' in rows[0] or "amount" in rows[0])

        # Check that we have the correct number of data rows
        self.assertEqual(len(rows), 3)  # Header + 2 data rows

    def test_admin_export_action(self):
        """Test the export action in the admin"""
        # Get the admin changelist URL
        url = reverse('admin:analytics_expense_changelist')

        # Select all expenses and trigger the export action
        post_data = {
            'action': 'export_route_as_csv',
            '_selected_action': [self.expense1.pk, self.expense2.pk],
        }
        response = self.client.post(url, post_data)

        # Check the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertTrue('attachment; filename=' in response['Content-Disposition'])
