from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from catalog.forms import ProductForm, ProductModeratorForm
from catalog.models import Product


class ProductListView(ListView):
    model = Product

class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product

    def get_object(self, queryset = None):
        self.object = super().get_object(queryset)
        self.object.views_counter += 1
        self.object.save()
        return self.object
        # self.object = super().get_object(queryset)
        # if self.request.user == self.object.owner:
        #     self.object.views_counter += 1
        #     self.object.save()
        #     return self.object
        # raise PermissionDenied


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        product = form.save()
        user = self.request.user
        product.owner = user
        product.save()
        return super().form_valid(form)

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_list')

    def get_success_url(self):
        return reverse('catalog:product_detail', args=[self.kwargs.get('pk')])

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return ProductForm
        if user.has_perm("catalog.can_delete_product"):
            return ProductForm
        raise PermissionDenied




class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:product_list')

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return ProductForm
        if user.has_perm("catalog.can_delete_product"):
            return ProductModeratorForm
        raise PermissionDenied

# class ProductUnpublishView(PermissionRequiredMixin, UpdateView):
#     model = Product
#     fields = ['status']
#     permission_required = 'catalog.can_unpublish_product'
#     template_name = 'catalog/product_unpublish.html'
#     success_url = reverse_lazy('catalog:product_list')
#
#     def form_valid(self, form):
#         product = form.save(commit=False)
#         product.status = 'unpublished'
#         product.save()
#         return super().form_valid(form)

class ProductUnpublishView(PermissionRequiredMixin, UpdateView):
    model = Product
    fields = ['status']
    permission_required = 'catalog.can_unpublish_product'
    template_name = 'catalog/product_unpublish.html'
    success_url = reverse_lazy('catalog:product_list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        user = self.request.user
        if user != user.has_perm('catalog.can_unpublish_product'):
            raise PermissionDenied("У вас нет прав для снятия продукта с публикации.")
        return obj

    def form_valid(self, form):
        product = form.save(commit=False)
        product.status = 'unpublished'
        product.save()
        return super().form_valid(form)