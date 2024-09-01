import { Link } from 'react-router-dom';

type Props = {
  id: number;
  image?: string[]; // Массив строк, предполагается, что это URL-ы изображений
  title: string;
  price: number;
};

const ProductItem: React.FC<Props> = ({ id, image, title, price }) => {
  return (
    <Link className='text-gray-700 cursor-pointer' to={`/product/${id}`}>
      <div className='overflow-hidden'>
        {image && image.length > 0 ? (
          <img className='hover:scale-110 transition ease-in-out' src={image[0]} alt={title} />
        ) : (
          <div className='h-48 w-full bg-gray-200 flex items-center justify-center'>
            <span>No Image Available</span>
          </div>
        )}
      </div>
      <p className='pt-3 pb-1 text-sm'>{title}</p>
      <p className='text-sm font-medium'>${price.toFixed(2)}</p>
    </Link>
  );
};

export default ProductItem;
