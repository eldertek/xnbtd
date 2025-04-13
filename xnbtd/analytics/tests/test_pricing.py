from datetime import date
from django.test import TestCase
from django.contrib.auth.models import User
from django.template import Context, Template

from xnbtd.tours.models import GLS, SHDEntry
from xnbtd.analytics.templatetags.pricing import (
    calculate_gls_delivered_packages_price,
    calculate_gls_pickup_packages_price,
    calculate_gls_shd_price,
    calculate_gls_total_price,
    get_month_gls_queryset
)


class GLSPricingTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        
        # Create test GLS entries for January 2023
        self.gls1 = GLS.objects.create(
            linked_user=self.user,
            name="GLS-001",
            date=date(2023, 1, 5),
            beginning_hour="08:00",
            ending_hour="17:00",
            license_plate="ABC123",
            points_charges=10,
            points_delivered=10,
            packages_charges=100,
            packages_delivered=95,
            avp_relay=2,
            packages_refused=3,
            eo=5,
            pickup_point=20,
            full_km=150
        )
        
        self.gls2 = GLS.objects.create(
            linked_user=self.user,
            name="GLS-002",
            date=date(2023, 1, 10),
            beginning_hour="08:00",
            ending_hour="17:00",
            license_plate="ABC123",
            points_charges=15,
            points_delivered=15,
            packages_charges=150,
            packages_delivered=145,
            avp_relay=3,
            packages_refused=2,
            eo=8,
            pickup_point=30,
            full_km=180
        )
        
        # Create test GLS entry for February 2023
        self.gls3 = GLS.objects.create(
            linked_user=self.user,
            name="GLS-003",
            date=date(2023, 2, 5),
            beginning_hour="08:00",
            ending_hour="17:00",
            license_plate="ABC123",
            points_charges=12,
            points_delivered=12,
            packages_charges=120,
            packages_delivered=115,
            avp_relay=2,
            packages_refused=3,
            eo=6,
            pickup_point=25,
            full_km=160
        )
        
        # Create SHD entries for the GLS objects
        SHDEntry.objects.create(gls=self.gls1, value=10)
        SHDEntry.objects.create(gls=self.gls1, value=5)
        SHDEntry.objects.create(gls=self.gls1, value=3)
        
        SHDEntry.objects.create(gls=self.gls2, value=8)
        SHDEntry.objects.create(gls=self.gls2, value=4)
        
        SHDEntry.objects.create(gls=self.gls3, value=12)
    
    def test_get_month_gls_queryset(self):
        """Test filtering GLS queryset by month"""
        all_gls = GLS.objects.all()
        
        # Test January 2023
        jan_queryset = get_month_gls_queryset(all_gls, 2023, 1)
        self.assertEqual(jan_queryset.count(), 2)
        self.assertIn(self.gls1, jan_queryset)
        self.assertIn(self.gls2, jan_queryset)
        self.assertNotIn(self.gls3, jan_queryset)
        
        # Test February 2023
        feb_queryset = get_month_gls_queryset(all_gls, 2023, 2)
        self.assertEqual(feb_queryset.count(), 1)
        self.assertIn(self.gls3, feb_queryset)
        
        # Test invalid month
        invalid_queryset = get_month_gls_queryset(all_gls, 2023, 13)
        self.assertEqual(invalid_queryset.count(), 0)
    
    def test_calculate_gls_delivered_packages_price_tier1(self):
        """Test pricing for delivered packages within tier 1 (≤ 18671)"""
        jan_queryset = get_month_gls_queryset(GLS.objects.all(), 2023, 1)
        
        # January: 95 + 145 = 240 packages (tier 1)
        price = calculate_gls_delivered_packages_price(jan_queryset)
        expected_price = 240 * 3.17
        self.assertEqual(price, round(expected_price, 2))
    
    def test_calculate_gls_delivered_packages_price_tier2(self):
        """Test pricing for delivered packages with tier 2 (> 18671)"""
        # Create a large delivery to test tier 2 pricing
        GLS.objects.create(
            linked_user=self.user,
            name="GLS-004",
            date=date(2023, 1, 15),
            beginning_hour="08:00",
            ending_hour="17:00",
            license_plate="ABC123",
            points_charges=1000,
            points_delivered=1000,
            packages_charges=19000,
            packages_delivered=18500,  # This will push total over tier 1 limit
            avp_relay=10,
            packages_refused=20,
            eo=15,
            pickup_point=50,
            full_km=500
        )
        
        jan_queryset = get_month_gls_queryset(GLS.objects.all(), 2023, 1)
        
        # January: 95 + 145 + 18500 = 18740 packages (tier 1 + tier 2)
        price = calculate_gls_delivered_packages_price(jan_queryset)
        
        # First 18671 packages at 3.17€
        tier1_price = 18671 * 3.17
        # Remaining 69 packages at 2.82€
        tier2_price = (18740 - 18671) * 2.82
        expected_price = tier1_price + tier2_price
        
        self.assertEqual(price, round(expected_price, 2))
    
    def test_calculate_gls_pickup_packages_price(self):
        """Test pricing for pickup packages"""
        jan_queryset = get_month_gls_queryset(GLS.objects.all(), 2023, 1)
        
        prices = calculate_gls_pickup_packages_price(jan_queryset)
        
        # Regular pickups: 20 + 30 = 50 at 1.52€ each
        expected_regular_price = 50 * 1.52
        # EO pickups: 5 + 8 = 13 at 1.5€ each
        expected_eo_price = 13 * 1.5
        expected_total = expected_regular_price + expected_eo_price
        
        self.assertEqual(prices['regular_pickup_price'], round(expected_regular_price, 2))
        self.assertEqual(prices['eo_price'], round(expected_eo_price, 2))
        self.assertEqual(prices['total_price'], round(expected_total, 2))
    
    def test_calculate_gls_shd_price(self):
        """Test pricing for SHD entries"""
        jan_queryset = get_month_gls_queryset(GLS.objects.all(), 2023, 1)
        
        price = calculate_gls_shd_price(jan_queryset)
        
        # GLS1: First SHD (10 * 3.17) + Second SHD (5 * 0.63) + Third SHD (3 * 0.32)
        gls1_price = (10 * 3.17) + (5 * 0.63) + (3 * 0.32)
        
        # GLS2: First SHD (8 * 3.17) + Second SHD (4 * 0.63)
        gls2_price = (8 * 3.17) + (4 * 0.63)
        
        expected_price = gls1_price + gls2_price
        
        self.assertEqual(price, round(expected_price, 2))
    
    def test_calculate_gls_total_price(self):
        """Test calculation of total GLS price"""
        jan_queryset = get_month_gls_queryset(GLS.objects.all(), 2023, 1)
        
        prices = calculate_gls_total_price(jan_queryset)
        
        # Delivered packages: 240 * 3.17 = 760.80
        delivered_price = 240 * 3.17
        
        # Regular pickups: 50 * 1.52 = 76.00
        regular_pickup_price = 50 * 1.52
        
        # EO pickups: 13 * 1.5 = 19.50
        eo_price = 13 * 1.5
        
        # SHD: (10 * 3.17) + (5 * 0.63) + (3 * 0.32) + (8 * 3.17) + (4 * 0.63)
        # = 31.7 + 3.15 + 0.96 + 25.36 + 2.52 = 63.69
        shd_price = (10 * 3.17) + (5 * 0.63) + (3 * 0.32) + (8 * 3.17) + (4 * 0.63)
        
        expected_total = delivered_price + regular_pickup_price + eo_price + shd_price
        
        self.assertEqual(prices['delivered_price'], round(delivered_price, 2))
        self.assertEqual(prices['regular_pickup_price'], round(regular_pickup_price, 2))
        self.assertEqual(prices['eo_price'], round(eo_price, 2))
        self.assertEqual(prices['shd_price'], round(shd_price, 2))
        self.assertEqual(prices['total_price'], round(expected_total, 2))
    
    def test_template_tags_in_template(self):
        """Test that the template tags work correctly in a template"""
        jan_queryset = get_month_gls_queryset(GLS.objects.all(), 2023, 1)
        
        template = Template(
            "{% load pricing %}"
            "{% calculate_gls_delivered_packages_price queryset as delivered_price %}"
            "{{ delivered_price }}"
        )
        
        context = Context({'queryset': jan_queryset})
        result = template.render(context)
        
        expected_price = 240 * 3.17
        self.assertEqual(float(result), round(expected_price, 2))
