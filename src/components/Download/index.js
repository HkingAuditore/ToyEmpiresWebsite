
import './styles.module.css';
import React, { useState } from 'react';
import {Button, ButtonGroup} from "@nextui-org/button";




export default function Download() {

  return (
    <div
        style={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          height: '50vh',
          fontSize: '20px',
        }}>
      <h1 className="header">现在下载</h1>
      <Button>Android</Button>
      <Button>Windows</Button>
      </div>
  );
}