import { MARKETPLACE_APP_PATH } from './Const';
import MarketplaceComponent from '@components/MarketplaceComponent';

export const MARKETPLACE_ROUTES = [
  {
    path: MARKETPLACE_APP_PATH,
    role: 'USER', // ROLES_CONSTANTS.USER,
    element: <MarketplaceComponent />, // TODO: страница маркетплейса основная
  },
];
