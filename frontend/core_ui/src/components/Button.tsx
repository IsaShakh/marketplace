import React, { ReactNode } from "react";
import { Button as AntButton } from "antd";

const CustomButton = ({ children }: { children: ReactNode }) => (
  <AntButton type="primary">{children}</AntButton>
);

export default CustomButton;
