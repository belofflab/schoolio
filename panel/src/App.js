import { Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Navbar from './containers/Navbar';
import { Container, CssBaseline, ThemeProvider } from "@mui/material";
import { createTheme } from "@mui/material/styles";
import './reset.css'
import { useEffect, useState } from 'react';
import { isAuthenticated } from './helpers/is_authenticated';

const appTheme = createTheme({
  appBar: {
    position: 'absolute',
    width: '100%',
    zIndex: '1400',
  }
})

function App() {
  const [authenticated, setAuthenticated] = useState(false);

  useEffect(() => {
    if (isAuthenticated()) {
      setAuthenticated(true);
    }
  }, [])
  return (
    <ThemeProvider theme={appTheme}>
      <CssBaseline enableColorScheme />
      <Navbar />
      <Container maxWidth='lg'>
        <Routes>
          <Route exact path='/' element={<Home authenticated={authenticated} />} />
        </Routes>
      </Container>
    </ThemeProvider>
  );
}

export default App;
