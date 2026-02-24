from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import F
from .models import Product, Warehouse, StockItem
from django.contrib.auth import login
from django.views.generic import FormView
from .forms import RegisterForm

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "inventory/home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx["product_count"] = Product.objects.count()
        ctx["warehouse_count"] = Warehouse.objects.count()
        ctx["stock_count"] = StockItem.objects.count()

        # low stock: quantity <= reorder_level
        ctx["low_stock_items"] = (
            StockItem.objects
            .select_related("product", "warehouse")
            .filter(quantity__lte=F("product__reorder_level"))
            .order_by("product__name")[:10]
        )
        return ctx
    
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.http import urlencode

    
class ProductListView(ListView):
    model = Product
    template_name = "inventory/product_list.html"
    context_object_name = "products"
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().order_by("name")
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(sku__icontains=q))
        return qs


class ProductDetailView(DetailView):
    model = Product
    template_name = "inventory/product_detail.html"
    context_object_name = "product"


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = ["sku", "name", "price", "reorder_level"]
    template_name = "inventory/product_form.html"
    success_url = reverse_lazy("product_list")


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    fields = ["sku", "name", "price", "reorder_level"]
    template_name = "inventory/product_form.html"
    success_url = reverse_lazy("product_list")


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = "inventory/product_confirm_delete.html"
    success_url = reverse_lazy("product_list")

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.conf import settings


from .models import Warehouse


class WarehouseListView(ListView):
    model = Warehouse
    template_name = "inventory/warehouse_list.html"
    context_object_name = "warehouses"


class WarehouseDetailView(DetailView):
    model = Warehouse
    template_name = "inventory/warehouse_detail.html"
    context_object_name = "warehouse"


class WarehouseCreateView(LoginRequiredMixin, CreateView):
    model = Warehouse
    fields = ["name", "city", "capacity"]
    template_name = "inventory/warehouse_form.html"
    success_url = reverse_lazy("warehouse_list")


class WarehouseUpdateView(LoginRequiredMixin, UpdateView):
    model = Warehouse
    fields = ["name", "city", "capacity"]
    template_name = "inventory/warehouse_form.html"
    success_url = reverse_lazy("warehouse_list")


class WarehouseDeleteView(LoginRequiredMixin, DeleteView):
    model = Warehouse
    template_name = "inventory/warehouse_confirm_delete.html"
    success_url = reverse_lazy("warehouse_list")

from django.db.models import Q

class StockItemListView(ListView):
    model = StockItem
    template_name = "inventory/stockitem_list.html"
    context_object_name = "stockitems"

    def get_queryset(self):
        qs = super().get_queryset().select_related("warehouse", "product").order_by("warehouse__name", "product__name")
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(
                Q(product__name__icontains=q) |
                Q(product__sku__icontains=q) |
                Q(warehouse__name__icontains=q) |
                Q(warehouse__city__icontains=q)
            )
        return qs


class StockItemDetailView(DetailView):
    model = StockItem
    template_name = "inventory/stockitem_detail.html"
    context_object_name = "stockitem"


class StockItemCreateView(LoginRequiredMixin, CreateView):
    model = StockItem
    fields = ["warehouse", "product", "quantity"]
    template_name = "inventory/stockitem_form.html"
    success_url = reverse_lazy("stockitem_list")


class StockItemUpdateView(LoginRequiredMixin, UpdateView):
    model = StockItem
    fields = ["warehouse", "product", "quantity"]
    template_name = "inventory/stockitem_form.html"
    success_url = reverse_lazy("stockitem_list")


class StockItemDeleteView(LoginRequiredMixin, DeleteView):
    model = StockItem
    template_name = "inventory/stockitem_confirm_delete.html"
    success_url = reverse_lazy("stockitem_list")

class RegisterView(FormView):
    template_name = "registration/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)