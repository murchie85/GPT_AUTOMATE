import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Line } from 'react-chartjs-2';

const CompareForexPairs = () => {
  const [forexPairs, setForexPairs] = useState([]);
  const [baseCurrency, setBaseCurrency] = useState('USD');
  const [quoteCurrency, setQuoteCurrency] = useState('CAD');
  const [data, setData] = useState({});

  useEffect(() => {
    async function fetchData() {
      const response = await axios.get(`/forex/${baseCurrency}/${quoteCurrency}`);
      setForexPairs(response.data);
    }
    fetchData();
  }, [baseCurrency, quoteCurrency]);

  useEffect(() => {
    function processData() {
      const labels = forexPairs.map((pair) => pair.date);
      const closePrices = forexPairs.map((pair) => pair.close);
      const openPrices = forexPairs.map((pair) => pair.open);

      setData({
        labels: labels,
        datasets: [
          {
            label: `${baseCurrency}/${quoteCurrency} Close`,
            data: closePrices,
            fill: false,
            borderColor: '#00FFFF'
          },
          {
            label: `${baseCurrency}/${quoteCurrency} Open`,
            data: openPrices,
            fill: false,
            borderColor: '#FFFF00'
          }
        ]
      });
    }

    processData();
  }, [forexPairs]);

  const handleBaseCurrencyChange = (event) => {
    setBaseCurrency(event.target.value);
  };

  const handleQuoteCurrencyChange = (event) => {
    setQuoteCurrency(event.target.value);
  };

  return (
    <div>
      <h1>Compare Forex Pairs</h1>
      <div>
        <label>
          Base Currency:
          <select value={baseCurrency} onChange={handleBaseCurrencyChange}>
            <option value="USD">USD</option>
            <option value="EUR">EUR</option>
            <option value="JPY">JPY</option>
            <option value="GBP">GBP</option>
          </select>
        </label>
        <label>
          Quote Currency:
          <select value={quoteCurrency} onChange={handleQuoteCurrencyChange}>
            <option value="CAD">CAD</option>
            <option value="MXN">MXN</option>
            <option value="AUD">AUD</option>
            <option value="CNY">CNY</option>
          </select>
        </label>
      </div>
      <div>
        <Line data={data} />
      </div>
    </div>
  );
};

export default CompareForexPairs;

##JOB_COMPLETE##