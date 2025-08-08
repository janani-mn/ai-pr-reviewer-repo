import React from 'react';

const CleanComponent = ({ title, items = [] }) => {
  const [selectedItem, setSelectedItem] = React.useState(null);

  const handleItemClick = React.useCallback((item) => {
    setSelectedItem(item);
  }, []);

  return (
    <div>
      <h2>{title}</h2>
      <ul>
        {items.map((item) => (
          <li
            key={item.id}
            onClick={() => handleItemClick(item)}
            style={{
              cursor: 'pointer',
              backgroundColor: selectedItem?.id === item.id ? '#e0e0e0' : 'transparent'
            }}
          >
            {item.name}
          </li>
        ))}
      </ul>
      {selectedItem && (
        <div>
          <h3>Selected: {selectedItem.name}</h3>
          <p>Description: {selectedItem.description}</p>
        </div>
      )}
    </div>
  );
};

export default React.memo(CleanComponent);
