import React, { useEffect, useState } from 'react';
import { productAPI } from '../services/api';
import { Search, ExternalLink, Package } from 'lucide-react';

const Products = () => {
  const [products, setProducts] = useState([]);
  const [filteredProducts, setFilteredProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    loadProducts();
  }, []);

  useEffect(() => {
    filterProducts();
  }, [searchTerm, products]);

  const loadProducts = async () => {
    try {
      const response = await productAPI.searchProducts();
      setProducts(response.data.products);
      setFilteredProducts(response.data.products);
    } catch (error) {
      console.error('Error loading products:', error);
    } finally {
      setLoading(false);
    }
  };

  const filterProducts = () => {
    if (!searchTerm) {
      setFilteredProducts(products);
      return;
    }

    const filtered = products.filter(product =>
      product.product_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      product.sku.toLowerCase().includes(searchTerm.toLowerCase()) ||
      product.category.toLowerCase().includes(searchTerm.toLowerCase())
    );

    setFilteredProducts(filtered);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold text-text">Product Catalog</h2>
        <p className="text-text-light mt-1">Browse available products for RFP matching</p>
      </div>

      {/* Search Bar */}
      <div className="bg-white rounded-lg shadow-md p-4">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-text-light" size={20} />
          <input
            type="text"
            placeholder="Search products by name, SKU, or category..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
          />
        </div>
      </div>

      {/* Product Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredProducts.length === 0 ? (
          <div className="col-span-full bg-white rounded-lg shadow-md p-12 text-center">
            <Package size={48} className="mx-auto text-text-light mb-4" />
            <p className="text-text-light">No products found</p>
          </div>
        ) : (
          filteredProducts.map((product) => (
            <div key={product.sku} className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow p-6">
              <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                  <span className="px-2 py-1 bg-primary/10 text-primary text-xs rounded font-medium">
                    {product.category}
                  </span>
                  <h3 className="text-lg font-bold text-text mt-2 line-clamp-2">
                    {product.product_name}
                  </h3>
                  <p className="text-sm text-text-light mt-1">SKU: {product.sku}</p>
                </div>
              </div>

              {/* Specifications */}
              <div className="space-y-2 mb-4">
                {product.specifications && Object.entries(product.specifications).slice(0, 4).map(([key, value]) => (
                  <div key={key} className="flex justify-between text-sm">
                    <span className="text-text-light">
                      {key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}:
                    </span>
                    <span className="text-text font-medium">{value}</span>
                  </div>
                ))}
              </div>

              {/* Price and Stock */}
              <div className="flex items-center justify-between pt-4 border-t border-gray-200">
                <div>
                  <p className="text-sm text-text-light">Unit Price</p>
                  <p className="text-xl font-bold text-primary">₹{product.unit_price}</p>
                </div>
                <span className={`px-3 py-1 rounded-full text-sm font-medium ${product.stock_status === 'In Stock'
                  ? 'bg-success/20 text-success'
                  : 'bg-error/20 text-error'
                  }`}>
                  {product.stock_status}
                </span>
              </div>

              {/* Datasheet Link */}
              {product.datasheet_url && (
                <a
                  href={product.datasheet_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center justify-center gap-2 mt-4 w-full px-4 py-2 border border-primary text-primary rounded-lg hover:bg-primary hover:text-white transition-colors"
                >
                  <ExternalLink size={16} />
                  View Datasheet
                </a>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default Products;
