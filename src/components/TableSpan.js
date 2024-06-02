import React from 'react';

export default function TableSpan({children, width}) {
  return (
    <div style={{width:width}}>
        {children}
    </div>

  );
}