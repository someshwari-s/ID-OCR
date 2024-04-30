import React, { useState, useEffect } from "react";
import axios from "axios";
import { Container, Row, Col, Spinner, Table } from "react-bootstrap";
import { toast, ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import aadharLogo from "./imce-logo.jpg";

function AadharCardUploader() {
  const [file, setFile] = useState(null);
  const [aadharNo, setAadharNo] = useState("");
  const [name, setName] = useState("");
  const [dob, setDob] = useState("");
  const [gender, setGender] = useState("");
  const [imagePreview, setImagePreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [aadharData, setAadharData] = useState([]);
  const [fetchClicked, setFetchClicked] = useState(false);

  // Function to refresh fields
  const refreshFields = () => {
    setAadharNo("");
    setName("");
    setDob("");
    setGender("");
  };

  // Function to handle file change
  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setImagePreview(URL.createObjectURL(e.target.files[0]));
  };

  // Function to handle upload
  const handleUpload = async () => {
    setLoading(true);
    const formData = new FormData();
    formData.append("image", file);

    try {
      const response = await axios.post(
        "http://localhost:5000/aadhar/extract_data",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      console.log("Response from backend:", response.data);

      const data = response.data;
      setAadharNo(data["Aadhar No"] || "");
      setName(data["Name"] || "");
      setDob(data["DOB"] || "");
      setGender(data["Gender"] || "");

      toast.success("Image uploaded successfully", {
        position: "top-center",
      });
    } catch (error) {
      console.error("Error uploading image:", error);
    } finally {
      setLoading(false);
    }
  };

  // Function to handle form submission
  const handleSubmit = async () => {
    try {
      setLoading(true);

      // Format date to YYYY-MM-DD
      const formattedDOB = dob.split("/").reverse().join("-");

      const response = await axios.post(
        "http://localhost:5000/aadhar/store_data",
        {
          "Aadhar No": aadharNo,
          Name: name,
          DOB: formattedDOB,
          Gender: gender,
        }
      );

      console.log("Response from database:", response.data);

      toast.success("Data inserted successfully", { position: "top-center" });

      // Clear form fields after submission
      refreshFields();
    } catch (error) {
      console.error("Error submitting data:", error);
      toast.error("Failed to insert data", { position: "top-center" });
    } finally {
      setLoading(false);
    }
  };

  // Function to handle fetching data
  const handleFetch = async () => {
    try {
      const response = await axios.get(
        "http://localhost:5000/aadhar/get_all_data"
      );
      setAadharData(response.data);
    } catch (error) {
      console.error("Error fetching data:", error);
      toast.error("Failed to fetch data", { position: "top-center" });
    }
  };

  useEffect(() => {
    if (fetchClicked) {
      handleFetch();
    }
  }, [fetchClicked]);

  return (
    <div style={{ position: "relative" }}>
      <ToastContainer position="top-center" />
      {loading && (
        <div
          style={{
            position: "fixed",
            top: 0,
            left: 0,
            width: "100%",
            height: "100%",
            backgroundColor: "rgba(255, 255, 255, 0.7)",
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            zIndex: 9999,
          }}
        >
          <Spinner animation="border" role="status" size="lg" />
        </div>
      )}
      <div
        style={{
          marginTop: "70px",
          border: "20px solid black",
          padding: "20px",
        }}
      >
        <Container>
          <center>
            <h1>Aadhar Card Recognizer</h1>
          </center>
          <br />
          <Row>
            <Col md={7} className="d-flex flex-column align-items-center">
              <h4>Upload Aadhar Card Image</h4>
              <div style={{ position: "relative", marginBottom: "20px" }}>
                {imagePreview ? (
                  <img
                    src={imagePreview}
                    alt="Selected Image"
                    style={{
                      width: "342px",
                      height: "200px",
                      objectFit: "cover",
                      marginBottom: "20px",
                    }}
                  />
                ) : (
                  <img
                    src={aadharLogo}
                    alt="Logo"
                    style={{
                      width: "200px",
                      height: "auto",
                      marginBottom: "20px",
                    }}
                  />
                )}
                <input
                  type="file"
                  onChange={handleFileChange}
                  style={{
                    position: "absolute",
                    top: "210px",
                    left: "70%",
                    transform: "translateX(-50%)",
                  }}
                />
              </div>
              <button
                onClick={handleUpload}
                style={{ marginTop: "10px", marginLeft: "16px" }}
                disabled={loading}
              >
                Upload
              </button>
            </Col>
            <Col md={5}>
              <div>
                <label style={{ display: "block", marginBottom: "10px" }}>
                  Aadhar No:
                  <input
                    type="text"
                    value={aadharNo}
                    onChange={(e) => setAadharNo(e.target.value)}
                    style={{ width: "100%", marginBottom: "10px" }}
                  />
                </label>
                <label style={{ display: "block", marginBottom: "10px" }}>
                  Name:
                  <input
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    style={{ width: "100%", marginBottom: "10px" }}
                  />
                </label>
                <label style={{ display: "block", marginBottom: "10px" }}>
                  Date of Birth:
                  <input
                    type="text"
                    value={dob}
                    onChange={(e) => setDob(e.target.value)}
                    style={{ width: "100%", marginBottom: "10px" }}
                  />
                </label>
                <label style={{ display: "block", marginBottom: "10px" }}>
                  Gender:
                  <input
                    type="text"
                    value={gender}
                    onChange={(e) => setGender(e.target.value)}
                    style={{ width: "100%", marginBottom: "10px" }}
                  />
                </label>
              </div>
              <button onClick={handleSubmit} style={{ marginTop: "10px" }}>
                Submit
              </button>
            </Col>
          </Row>
          <Row>
            <Col>
              <button
                onClick={() => setFetchClicked(true)}
                style={{ margin: "10px 60px", padding: "6px" }}
              >
                Fetch
              </button>
            </Col>
          </Row>
          {aadharData.length > 0 && (
            <Row>
              <Col>
                <Table striped bordered hover>
                  <thead>
                    <tr>
                      <th>Aadhar No</th>
                      <th>Name</th>
                      <th>Date of Birth</th>
                      <th>Gender</th>
                    </tr>
                  </thead>
                  <tbody>
                    {aadharData.map((item, index) => (
                      <tr key={index}>
                        <td>{item.user_aadhar_no}</td>
                        <td>{item.user_name}</td>
                        <td>{item.user_dob}</td>
                        <td>{item.user_gender}</td>
                      </tr>
                    ))}
                  </tbody>
                </Table>
              </Col>
            </Row>
          )}
        </Container>
      </div>
    </div>
  );
}

export default AadharCardUploader;
