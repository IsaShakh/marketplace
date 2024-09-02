import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

type ProductData = {
  id: number;
  title: string;
  price: number;
  description: string;
  images: { image: string }[];
  size: number;
  amount: number;
  condition: string;
};

const Product = (props: Props) => {
  const { productId } = useParams();
  const [productData, setProductData] = useState<ProductData | null>(null);
  const [image, setImage] = useState<string>('');
  const [selectedSize, setSelectedSize] = useState<number | null>(null);

  const fetchProductData = async () => {
    try {
      const response = await fetch(`http://localhost:8000/api/v1/products/${productId}/`);
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data: ProductData = await response.json();
      setProductData(data);
      setImage(data.images[0]?.image || 'https://via.placeholder.com/500'); // Используем заглушку, если изображение отсутствует
      setSelectedSize(data.size || null);
    } catch (error) {
      console.error('Error fetching product data:', error);
    }
  };

  useEffect(() => {
    fetchProductData();
  }, [productId]);

  if (!productData) {
    return <div>Loading...</div>;
  }

  return (
    <div className="border-t-2 pt-10 transition-opacity ease-in duration-500 opacity-100">
      <div className="flex gap-12 sm:gap-12 flex-col sm:flex-row">
        {/* Images */}
        <div className="flex-1 flex flex-col-reverse gap-3 sm:flex-row">
          <div className="flex sm:flex-col overflow-x-auto sm:overflow-y-scroll justify-between sm:justify-normal sm:w-[18.7%] w-full">
            {productData.images.map((item, index) => (
              <img
                onClick={() => setImage(item.image)}
                src={item.image || 'https://via.placeholder.com/500'} // Используем заглушку, если изображение отсутствует
                alt=""
                key={index}
                className="w-[24%] sm:w-full sm:mb-3 flex-shrink-0 cursor-pointer"
                onError={(e) => (e.currentTarget.src = 'https://via.placeholder.com/500')} // Подменяем на заглушку при ошибке загрузки
              />
            ))}
          </div>
          <div className="w-full sm:w-[80%]">
            <img src={image} alt="" className="w-full h-auto" onError={(e) => (e.currentTarget.src = 'https://via.placeholder.com/500')} />
          </div>
        </div>
        {/* Info */}
        <div className="flex-1">
          <h1 className="font-medium text-2xl mt-2">{productData.title}</h1>
          <p className="mt-5 text-3xl font-medium">${productData.price}</p>
          <p className="mt-5 text-gray-600 md:w-4/5">{productData.description || 'No description available.'}</p>
          <div className="flex flex-col gap-4 my-8">
            <p>Select size</p>
            <div className="flex gap-2">
              <button
                onClick={() => setSelectedSize(productData.size)}
                className={`border py-2 px-4 bg-gray-100 ${productData.size === selectedSize ? 'border-orange-500' : ''}`}
              >
                {productData.size}
              </button>
            </div>
          </div>
          <button className="bg-black text-white px-8 py-3 text-sm active:bg-gray-700">Add to cart</button>
          <hr className="mt-8 sm:w-4/5" />
          <div className="text-sm text-gray-600 mt-5 flex flex-col gap-1">
            <p>Product ID: {productData.id}</p>
            <p>Amount available: {productData.amount}</p>
            <p>Condition: {productData.condition}</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Product;
