import "./App.css";
import TextField from "@mui/material/TextField";
import { useEffect, useState } from "react";
import { hardcodedResponse } from "./heatmapData";
import { useDebounce } from "@uidotdev/usehooks";
import Heatmap from "./components/Heatmap";
import TokenVisualizer from "./components/TokenVisualizer";
import NextWordTable from "./components/NextWordTable";
import LoadingOverlay from "./LoadingOverlay";

function App() {
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState();

  const debouncedText = useDebounce(text, 500);

  useEffect(() => {
    if (!debouncedText) {
      setResponse({});
      return;
    }
    const asyncEffect = async () => {
      setLoading(true);
      await fetchData();
      setLoading(false);
    };
    asyncEffect();
  }, [debouncedText]);

  const fetchData = async () => {
    if (!process.env.REACT_APP_POST_ENDPOINT) return hardcodedResponse;
    try {
      const apiResponse = await fetch(process.env.REACT_APP_POST_ENDPOINT, {
        method: "POST",
        mode: "cors",
        cache: "no-cache",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
        redirect: "follow",
        referrerPolicy: "no-referrer", // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
        body: JSON.stringify({ userInput: debouncedText }), // body data type must match "Content-Type" header
      });
      const r = JSON.parse(await apiResponse?.json());
      console.log(r);
      setResponse(r);
    } catch (e) {
      console.log(e);
      return hardcodedResponse;
    }
  };

  const onTokenPress = (e) => {
    setText(`${text}${e}`);
  };

  return (
    <div className="app-container">
      <div className="top-section">
        <div>
          <TextField
            label="Input"
            autoFocus
            placeholder="Type here"
            variant="outlined"
            multiline
            minRows={10}
            inputProps={{ maxLength: 2500 }}
            value={text}
            onChange={(e) => setText(e.target.value)}
          />
        </div>
        <div class="top-right-section">
          <TokenVisualizer data={response?.tokens} />
          <NextWordTable data={response?.logits} onTokenPress={onTokenPress} />
        </div>
      </div>
      <div className="bottom-section">
        <Heatmap
          domId="embedding"
          data={response?.embedding}
          toColor="#38C415"
          displayName="Embedding"
        />
        <Heatmap
          domId="context"
          data={response?.context}
          displayName="Context"
        />
      </div>
      {loading && <LoadingOverlay />}
    </div>
  );
}

export default App;
