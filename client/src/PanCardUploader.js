import React, { useState, useEffect } from "react";
import axios from "axios";
import { Container, Row, Col, Spinner } from "react-bootstrap";
import logo from "./imce-logo.jpg";
import { toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { ToastContainer } from "react-toastify";

function PanCardUploader() {
  const [file, setFile] = useState(null);
  const [data, setData] = useState([]);
  const [fatherName, setFatherName] = useState("");
  const [dob, setDob] = useState("");
  const [name, setName] = useState("");
  const [panNo, setPanNo] = useState("");
  const [imagePreview, setImagePreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [fetchClicked, setFetchClicked] = useState(false);

  const handleFetchData = async () => {
    setLoading(true);
    try {
      const response = await axios.get(
        "http://localhost:5000/pan/get_all_data"
      );
      setData(response.data);
      toast.success("Data fetched successfully", { position: "top-center" });
    } catch (error) {
      console.error("Error fetching data:", error);
      toast.error("Failed to fetch data", { position: "top-center" });
    } finally {
      setLoading(false);
    }
  };

  const handleFetchClick = () => {
    handleFetchData();
    setFetchClicked(true);
  };

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setImagePreview(URL.createObjectURL(e.target.files[0]));
  };

  const handleUpload = async () => {
    setLoading(true);
    const formData = new FormData();
    formData.append("image", file);

    try {
      const response = await axios.post(
        "http://localhost:5000/pan/extract_data",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      setPanNo(response.data["pan no"]);
      setDob(response.data["Date of Birth"]);
      setName(response.data["Name"]);
      setFatherName(response.data["Father name"]);
      toast.success("Image uploaded successfully", {
        position: "top-center",
      });
    } catch (error) {
      console.error("Error uploading image:", error);
      toast.error("Failed to upload image", { position: "top-center" });
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async () => {
    await handleUpload();

    const data = {
      "pan no": panNo,
      "Date of Birth": dob,
      Name: name,
      "Father name": fatherName,
    };

    try {
      await axios.post("http://localhost:5000/pan/store_data", data);
      toast.success("Data submitted successfully", { position: "top-center" });
    } catch (error) {
      console.error("Error submitting data:", error);
      toast.error("Failed to submit data", { position: "top-center" });
    }
  };

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
            <h1>PanCard Recognizer</h1>
          </center>
          <br />
          <Row>
            <Col md={7} className="d-flex flex-column align-items-center">
              <h4>Upload PAN Card Image</h4>
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
                    src={logo}
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
                  PAN No:
                  <input
                    type="text"
                    value={panNo}
                    onChange={(e) => setPanNo(e.target.value)}
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
                  Father's Name:
                  <input
                    type="text"
                    value={fatherName}
                    onChange={(e) => setFatherName(e.target.value)}
                    style={{ width: "100%", marginBottom: "10px" }}
                  />
                </label>
                <label style={{ display: "block", marginBottom: "10px" }}>
                  Date of Birth:
                  <input
                    type="date"
                    value={dob}
                    onChange={(e) => setDob(e.target.value)}
                    style={{ width: "100%", marginBottom: "10px" }}
                  />
                </label>
                <button onClick={handleSubmit}>Submit</button>
              </div>
            </Col>
          </Row>
        </Container>
      </div>
      <div style={{ marginTop: "20px", textAlign: "center" }}>
        <button onClick={handleFetchClick}>Fetch</button>
      </div>

      {fetchClicked && (
        <div style={{ marginTop: "20px", textAlign: "center" }}>
          <h2>Fetched Data</h2>
          {loading ? (
            <Spinner animation="border" role="status" />
          ) : (
            <table
              style={{
                margin: "auto",
                borderCollapse: "collapse",
                border: "1px solid black",
              }}
            >
              <thead>
                <tr>
                  <th style={{ padding: "8px", border: "1px solid black" }}>
                    PAN No
                  </th>
                  <th style={{ padding: "8px", border: "1px solid black" }}>
                    Name
                  </th>
                  <th style={{ padding: "8px", border: "1px solid black" }}>
                    Father's Name
                  </th>
                  <th style={{ padding: "8px", border: "1px solid black" }}>
                    Date of Birth
                  </th>
                </tr>
              </thead>
              <tbody>
                {data.map((item, index) => (
                  <tr key={index}>
                    <td style={{ padding: "8px", border: "1px solid black" }}>
                      {item.user_pan_no}
                    </td>
                    <td style={{ padding: "8px", border: "1px solid black" }}>
                      {item.user_name}
                    </td>
                    <td style={{ padding: "8px", border: "1px solid black" }}>
                      {item.user_father_name}
                    </td>
                    <td style={{ padding: "8px", border: "1px solid black" }}>
                      {item.user_dob}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      )}
    </div>
  );
}

export default PanCardUploader;
