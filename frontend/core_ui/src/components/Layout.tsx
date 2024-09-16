import { ReactNode } from "react";
import { Layout as AntLayout } from "antd";

const { Header, Content, Footer } = AntLayout;

const CustomLayout = ({ children }: { children: ReactNode }) => (
  <AntLayout>
    <Header>Core UI Header</Header>
    <Content>{children}</Content>
    <Footer>Core UI Footer</Footer>
  </AntLayout>
);

export default CustomLayout;
