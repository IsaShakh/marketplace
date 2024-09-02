import { useEffect, useState, useContext } from "react";
import { SearchContext } from "@/context/SearchContext";
import Title from "@/components/Title";
import ProductItem from "@/components/ProductItem";

type Product = {
  id: number;
  title: string;
  price: number;
  image: string;
};

type Category = {
  id: number;
  name: string;
  parent: number | null;
};

type Style = {
  id: number;
  name: string;
};

const Products = () => {
  const { search } = useContext(SearchContext); // Получаем значение поиска из контекста

  const [showFilter, setShowFilter] = useState(false);
  const [filterProducts, setFilterProducts] = useState<Product[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [styles, setStyles] = useState<Style[]>([]);
  const [openCategories, setOpenCategories] = useState<number[]>([]);
  const [selectedCategories, setSelectedCategories] = useState<number[]>([]);
  const [selectedStyles, setSelectedStyles] = useState<number[]>([]);
  const [nextPage, setNextPage] = useState<string | null>("http://localhost:8000/api/v1/products/");
  const [loading, setLoading] = useState<boolean>(false);
  const [sortType, setSortType] = useState<string>('relavent');

  const toggleCategory = (categoryId: number) => {
    if (openCategories.includes(categoryId)) {
      setOpenCategories(openCategories.filter(id => id !== categoryId));
    } else {
      setOpenCategories([...openCategories, categoryId]);
    }
  };

  const handleSubcategorySelect = (subcategoryId: number, parentCategoryId: number | null) => {
    setSelectedCategories(prev => {
      const newSelection = prev.includes(subcategoryId)
        ? prev.filter(id => id !== subcategoryId)
        : [...prev, subcategoryId];

      const siblingSubcategories = categories.filter(category => category.parent === parentCategoryId).map(cat => cat.id);
      const isAnySiblingSelected = siblingSubcategories.some(id => newSelection.includes(id));

      return isAnySiblingSelected
        ? newSelection
        : newSelection.filter(id => id !== parentCategoryId);
    });
  };

  const handleViewAll = (categoryId: number) => {
    setSelectedCategories([categoryId]);
  };

  const toggleStyle = (styleId: number) => {
    setSelectedStyles(prev =>
      prev.includes(styleId)
        ? prev.filter(id => id !== styleId)
        : [...prev, styleId]
    );
  };

  const fetchProducts = async (url: string, append: boolean = false) => {
    if (loading || !url) return;

    setLoading(true);
    try {
      const response = await fetch(url);
      const data = await response.json();

      if (Array.isArray(data.results)) {
        if (append) {
          setFilterProducts(prevProducts => [...prevProducts, ...data.results]);
        } else {
          setFilterProducts(data.results);
        }
        setNextPage(data.next);
      }
    } catch (error) {
      console.error('Error fetching products:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const url = `http://localhost:8000/api/v1/products/?category=${selectedCategories.join(',')}&style=${selectedStyles.join(',')}&ordering=${sortType === 'low-high' ? 'price' : sortType === 'high-low' ? '-price' : ''}&search=${search}`; // Добавляем параметр поиска в URL
    setFilterProducts([]); 
    fetchProducts(url);
  }, [selectedCategories, selectedStyles, sortType, search]); // Добавляем `search` в зависимости

  useEffect(() => {
    fetchProducts(nextPage!);
  }, []);

  useEffect(() => {
    const handleScroll = () => {
      if (window.innerHeight + document.documentElement.scrollTop >= document.documentElement.offsetHeight - 500 && nextPage && !loading) {
        fetchProducts(nextPage, true);
      }
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, [nextPage, loading]);

  useEffect(() => {
    const fetchCategoriesAndStyles = async () => {
      try {
        const [categoriesResponse, stylesResponse] = await Promise.all([
          fetch('http://localhost:8000/api/v1/categories/'),
          fetch('http://localhost:8000/api/v1/styles/')
        ]);

        const categoriesData = await categoriesResponse.json();
        const stylesData = await stylesResponse.json();

        setCategories(categoriesData);
        setStyles(stylesData);
      } catch (error) {
        console.error('Error fetching categories and styles:', error);
      }
    };

    fetchCategoriesAndStyles();
  }, []);

  const renderCategories = (parentId: number | null) => {
    return categories
      .filter(category => category.parent === parentId)
      .map(category => (
        <div key={category.id} style={{ marginLeft: parentId ? "20px" : "0px" }}>
          {parentId === null ? (
            <div>
              <p onClick={() => toggleCategory(category.id)} style={{ cursor: "pointer", fontWeight: "bold" }}>
                {category.name} {openCategories.includes(category.id) ? "-" : "+"}
              </p>
              {openCategories.includes(category.id) && (
                <div>
                  {renderCategories(category.id)}
                  <button onClick={() => handleViewAll(category.id)} style={{ marginLeft: "20px" }}>
                    Посмотреть все
                  </button>
                </div>
              )}
            </div>
          ) : (
            <div>
              <p>
                <label>
                  <input
                    type="checkbox"
                    onChange={() => handleSubcategorySelect(category.id, category.parent)}
                    checked={selectedCategories.includes(category.id)}
                  />
                  {category.name}
                </label>
              </p>
            </div>
          )}
        </div>
      ));
  };

  return (
    <div className="flex flex-col sm:flex-row gap-1 sm:gap-10 pt-10 border-t">
      {/* Filters */}
      <div className="min-w-60">
        <p className="my-2 text-xl flex items-center cursor-pointer gap-2" onClick={() => setShowFilter(!showFilter)}>
          FILTERS
        </p>
        <div className={`border border-gray-300 pl-5 py-3 mt-6 ${showFilter ? '' : 'hidden'} sm:block`}>
          <p className="mb-3 text-sm font-medium">CATEGORIES</p>
          <div className="flex flex-col gap-2 text-sm font-light text-gray-700">
            {renderCategories(null)}
          </div>
        </div>
        <div className={`border border-gray-300 pl-5 py-3 mt-6 ${showFilter ? '' : 'hidden'} sm:block`}>
          <p className="mb-3 text-sm font-medium">STYLES</p>
          <div className="flex flex-col gap-2 text-sm font-light text-gray-700">
            {styles.map(style => (
              <p key={style.id} className="flex gap-2">
                <input
                  type="checkbox"
                  className="w-3"
                  value={style.id}
                  onChange={() => toggleStyle(style.id)}
                /> {style.name}
              </p>
            ))}
          </div>
        </div>
      </div>
      {/* Right side */}
      <div className="flex-1">
        <div className="flex justify-between text-base sm:text-2xl mb-4">
          <Title text1={'ALL'} text2={'PRODUCTS'} />
          <select
            className="border-2 border-gray-300 text-sm px-2"
            value={sortType}
            onChange={(e) => setSortType(e.target.value)}
          >
            <option value="relavent">Sort by: Relevant</option>
            <option value="low-high">Sort by: Low-to-High</option>
            <option value="high-low">Sort by: High-to-Low</option>
          </select>
        </div>
        {/* Products */}
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 gap-y-6">
          {filterProducts
            .map((item) => (
              <ProductItem
                key={item.id}
                title={item.title}
                id={item.id}
                price={item.price}
                image={item.image}
              />
            ))}
        </div>
        {loading && <div>Loading more products...</div>}
      </div>
    </div>
  );
};

export default Products;
