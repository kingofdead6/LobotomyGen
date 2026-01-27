import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import ApiKeyPage from "./components/ApiKeyPage";
import GeneratePage from "./components/GeneratePage";


function App() {
  return (
    <Router>
      <Routes>
          <Route path="/" element={<ApiKeyPage />} />
          <Route path="/generate" element={<GeneratePage />}/>
      </Routes>
    </Router>
  );
}

export default App;