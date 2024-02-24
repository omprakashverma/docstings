import React from "react";
import axios from "axios";
import { Container, Paper } from "@mui/material";
import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button";
import Grid from "@mui/material/Grid";
import banner from "./images/banner.png";
import CircularProgress from "@mui/material/CircularProgress";
import { green } from "@mui/material/colors";
import Fab from "@mui/material/Fab";
import CheckIcon from "@mui/icons-material/Check";

const myStyle = {
  backgroundImage: banner,
};
export default function App() {
  const [loading, setLoading] = React.useState(false);
  const [success, setSuccess] = React.useState(false);
  const [progress, setProgress] = React.useState(0);
  const [formData, setFormData] = React.useState({
    destination_repo: "",
    module_name: "",
  });

  const buttonSx = {
    ...(success && {
      bgcolor: green[500],
      "&:hover": {
        bgcolor: green[700],
      },
    }),
  };

  const Header = () => {
    return (
      <>
        <div>
          <Grid container justifyContent="left">
            <Grid item xs={1}>
              {/* <img src={logo} alt="Logo" height={70}  width={200}  /> */}
            </Grid>
            <Grid item xs={9}>
              <h1 style={{ textAlign: "center", color: "rgb(253, 95, 7)" }}>
                Semicolons 2024
              </h1>
            </Grid>
            <Grid item xs={2} justifyContent="right">
              <h3 style={{ textAlign: "center", color: "rgb(253, 95, 7)" }}>
                TEAM NAKSHATRA
              </h3>
            </Grid>
          </Grid>
        </div>
      </>
    );
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  // Set interval to make API call every 5 seconds
  const interval = setInterval(() => {
    fetchDataStatus();
  }, 5000);
  const fetchDataStatus = async () => {
    try {
      // Make API call here
      const response = await fetch("https://api.example.com/data");
      const data = await response.json();
      setProgress(data);
      console.log(data);
      //  clearInterval(interval);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setSuccess(false);
    setLoading(true);
    fetchDataStatus();
    console.log("formData", formData);
    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/start_execution",
        formData,
        {
          headers: {
            Accept: "application/json",
          },
        }
      );
      console.log(response.data);
      setSuccess(true);
      setLoading(false);
    } catch (error) {
      setSuccess(false);
      setLoading(false);
      console.error("error", error);
    }
  };

  return (
    <>
      <Container style={myStyle}>
        <Header></Header>
        <Paper elevation={0}>
          <h3>Accelerating Development with AI-Powered Doc String</h3>
          <em>Boost Productivity, Enhance Code Quality</em>
          <form onSubmit={handleSubmit}>
            <Grid container spacing={2} m={2} pt={3}>
              <Grid item xs={3}>
                <TextField
                  value={formData.destination_repo}
                  onChange={handleChange}
                  name="destination_repo"
                  id="destination_repo"
                  label="Please enter repository path"
                  variant="outlined"
                />
              </Grid>
              <Grid item xs={3}>
                <TextField
                  value={formData.module_name}
                  onChange={handleChange}
                  name="module_name"
                  id="module_name"
                  label="Please enter package name "
                  variant="outlined"
                />
              </Grid>
              <Grid item xs={4} style={{ position: "relative" }}>
                <Fab aria-label="save" color="primary" sx={buttonSx}>
                  {success ? <CheckIcon /> : <h2>{progress}</h2>}
                </Fab>

                {loading && (
                  <CircularProgress
                    size={68}
                    sx={{
                      color: green[500],
                      position: "absolute",
                      top: 10,
                      left: 10,
                      zIndex: 1,
                    }}
                  />
                )}
                <Button
                  style={{ marginLeft: "10px" }}
                  type="submit"
                  variant="contained"
                >
                  Generate document
                </Button>
              </Grid>
            </Grid>
          </form>
          {formData.destination_repo && (
            <p>
              Please find document at url:{" "}
              {formData.destination_repo + "/build/index.html"}
            </p>
          )}
        </Paper>
      </Container>
    </>
  );
}
