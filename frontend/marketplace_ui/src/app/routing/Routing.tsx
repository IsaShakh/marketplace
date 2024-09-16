import { FC } from 'react';
import { Navigate, Route, Routes } from 'react-router-dom';
import { MARKETPLACE_ROUTES } from './Routes';
import { PrivateRoute } from '@shared';
import MarketplaceComponent from '@components/MarketplaceComponent';

const AppRouting: FC = () => (
  <Routes>
    <Route path="/" element={<Navigate to="/market" />} />
    {MARKETPLACE_ROUTES.map((route) =>
      Array.isArray(route.path) ? (
        route.path.map((p) => (
          <Route
            key={route.path}
            element={<PrivateRoute children={route.element} role={p.role} />}
            path={p.path}
          />
        ))
      ) : (
        <Route
          key={route.path}
          path={route.path}
          element={<PrivateRoute children={route.element} role={route.role} />}
        />
      ),
    )}
  </Routes>
);

export default AppRouting;
