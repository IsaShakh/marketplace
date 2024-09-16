import { FC } from 'react';
import { NoAccess } from '@shared';

interface IPrivateRoute {
  children: JSX.Element;
  role?: string;
}

const PrivateRoute: FC<IPrivateRoute> = ({ children, role }) => {
  const isAccess = role === 'USER'; // TODO: описать хук понимающий есть ли доступ к странице или нет

  return isAccess ? children : <NoAccess />;
};

export default PrivateRoute;
