import React, {useEffect, useState} from 'react';
import axios from 'axios';

function App(){
  const [products, setProducts] = useState([]);

  //This function runs when the page loads
  useEffect(() => {
    //Attempt to fetch data Django API
    axios.get('http://127.0.0.1:8000/api/products/')
      .then(response => {
        console.log("Data fetched:", response.data);
        setProducts(response.data);
      })
      .catch(error => {
        console.error("Error connecting to Django:",error);
      });
  },[]);

  return (
    <div style={{ padding: "20px" }}>
      <h1>SupplyFlow Connection Test</h1>
      <p>If you see products below, React is talking to Django!</p>

      <ul>
        {products.map(product => (
          <li key={product.id}>
            <strong>{product.name}</strong>-${product.price}
            <br />
            {product.image && <img src={product.image} alt={product.name} width="100" />}

          </li>
        ))}
      </ul>

    </div>
  );
}

export default App;