import { Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Navbar from './containers/Navbar';
import { CssBaseline, ThemeProvider } from "@mui/material";
import { createTheme } from "@mui/material/styles";
import './reset.css'

const appTheme = createTheme({
  appBar: {
    position: 'absolute',
    width: '100%',
    zIndex: '1400',
  },
})

function App() {
  return (
    <ThemeProvider theme={appTheme}>
      <CssBaseline enableColorScheme />
      <Navbar />
      <Routes>
        <Route exact path='/' element={<Home />} />
      </Routes>
    </ThemeProvider>
  );
}

export default App;
