import React, {
  useState,
  useEffect
} from "react";

import {
  Container,
  Row,
  Col,
  Card,
  CardBody,
  Button
} from "reactstrap";

import DemoNavbar from "components/Navbars/DemoNavbar.js";
import CardsFooter from "components/Footers/CardsFooter.js";

export default function ThemeShop() {

  const [message, setMessage] =
    useState("");

  const buyTheme = async (
    themeName
  ) => {

    const loginId =
      localStorage.getItem(
        "loginId"
      );

    const response =
      await fetch(
        `http://127.0.0.1:8000/buy-theme?login_id=${loginId}&theme_name=${themeName}`,
        {
          method: "POST"
        }
      );

    const data =
      await response.json();

    setMessage(
      data.message
    );
  };

  const applyTheme = async (
    themeName
  ) => {

    const loginId =
      localStorage.getItem(
        "loginId"
      );

    const response =
      await fetch(
        `http://127.0.0.1:8000/apply-theme?login_id=${loginId}&theme_name=${themeName}`,
        {
          method: "POST"
        }
      );

    const result =
      await response.json();

    setMessage(
      result.message
    );

    setThemes({
        ...themes,
        selected_theme:
            themeName
    });

    localStorage.setItem(
      "selectedTheme",
      themeName
    );
  };

    const [themes, setThemes] =
        useState({
            selected_theme:
            localStorage.getItem(
                "selectedTheme"
        ) || "default"
    });

  useEffect(() => {

    const loginId =
      localStorage.getItem(
        "loginId"
      );

    fetch(
      `http://127.0.0.1:8000/themes?login_id=${loginId}`
    )
      .then((response) =>
        response.json()
      )
      .then((data) => {
        setThemes(data);
      });

  }, []);

  return (
    <>
      <DemoNavbar />

      <main>
        <section className="section section-shaped section-lg">
          <div
            className="shape shape-style-1"
            style={{
              background:
                themes?.selected_theme === "pink"
                  ? "linear-gradient(150deg,#ffb6c1 15%,#ff8fab 70%,#ff5e8a 94%)"
                  : themes?.selected_theme === "purple"
                  ? "linear-gradient(150deg,#c8a2ff 15%,#a66cff 70%,#8b4dff 94%)"
                  : themes?.selected_theme === "blue"
                  ? "linear-gradient(150deg,#7795f8 15%,#6772e5 70%,#555abf 94%)"
                  : "linear-gradient(150deg,#172b4d 15%,#1a174d 70%,#22204d 94%)"
            }}
          >
            <span />
            <span />
            <span />
            <span />
            <span />
            <span />
            <span />
            <span />
          </div>

          <Container className="pt-lg-7">
            <Row className="justify-content-center">
              <Col lg="10">
                <Card className="shadow border-0">
                  <CardBody className="p-5">

                    <h3 className="font-weight-bold">
                      🎨 테마 상점
                    </h3>

                    <p className="text-muted">
                      포인트를 사용하여 원하는 테마를 구매할 수 있습니다.
                    </p>

                    {message && (
                        <p
                            className="mt-3"
                            style={{
                                color: "#2dce89",
                                fontWeight: "bold"
                            }}
                        >
                            {message}
                        </p>
                    )}

                    <Row className="mt-5">

                      {/* 기본 테마 */}
                      <Col md="6" className="mb-4">
                        <Card className="shadow">
                          <CardBody className="text-center">

                            <div
                              style={{
                                height: "140px",
                                background: "linear-gradient(150deg,#172b4d 15%,#1a174d 70%,#22204d 94%)",
                                borderRadius: "10px"
                              }}
                            />

                            <h5 className="mt-3">
                              기본 테마
                            </h5>

                            <p className="text-muted">
                              무료
                            </p>

                            <Button
                              onClick={() =>
                                applyTheme("default")
                              }
                              style={{
                                backgroundColor: "#172b4d",
                                borderColor: "#172b4d",
                                color: "white"
                              }}
                            >
                              적용
                            </Button>

                          </CardBody>
                        </Card>
                      </Col>

                      {/* 핑크 테마 */}
                      <Col md="6" className="mb-4">
                        <Card className="shadow">
                          <CardBody className="text-center">

                            <div
                              style={{
                                height: "140px",
                                background: "#FFD6E7",
                                borderRadius: "10px"
                              }}
                            />

                            <h5 className="mt-3">
                              핑크 테마
                            </h5>

                            <p className="text-muted">
                              500P
                            </p>

                            {themes?.pink_theme ? (
                                <Button
                                    onClick={() =>
                                        applyTheme("pink")
                                    }
                                    style={{
                                        backgroundColor: "#FF5E8A",
                                        borderColor: "#FF5E8A",
                                        color: "white"
                                    }}
                                >
                                    적용
                                </Button>
                            ) : (
                                <Button
                                    onClick={() =>
                                        buyTheme("pink")
                                    }
                                    style={{
                                        backgroundColor: "#FF5E8A",
                                        borderColor: "#FF5E8A",
                                        color: "white"
                                    }}
                                >
                                    구매
                                </Button>
                              )}

                          </CardBody>
                        </Card>
                      </Col>

                      {/* 블루 테마 */}
                      <Col md="6" className="mb-4">
                        <Card className="shadow">
                          <CardBody className="text-center">

                            <div
                              style={{
                                height: "140px",
                                background: "#D6E8FF",
                                borderRadius: "10px"
                              }}
                            />

                            <h5 className="mt-3">
                              블루 테마
                            </h5>

                            <p className="text-muted">
                              500P
                            </p>

                            {themes?.blue_theme ? (
                                <Button
                                    onClick={() =>
                                        applyTheme("blue")
                                    }
                                    style={{
                                        backgroundColor: "#4F7BFF",
                                        borderColor: "#4F7BFF",
                                        color: "white"
                                    }}
                                >
                                    적용
                                </Button>
                            ) : (
                                <Button
                                    onClick={() =>
                                        buyTheme("blue")
                                    }
                                    style={{
                                        backgroundColor: "#4F7BFF",
                                        borderColor: "#4F7BFF",
                                        color: "white"
                                    }}
                                >
                                    구매
                                </Button>
                              )}

                          </CardBody>
                        </Card>
                      </Col>

                      {/* 퍼플 테마 */}
                      <Col md="6" className="mb-4">
                        <Card className="shadow">
                          <CardBody className="text-center">

                            <div
                              style={{
                                height: "140px",
                                background: "#E7D6FF",
                                borderRadius: "10px"
                              }}
                            />

                            <h5 className="mt-3">
                              퍼플 테마
                            </h5>

                            <p className="text-muted">
                              500P
                            </p>

                            {themes?.purple_theme ? (
                                <Button
                                    onClick={() =>
                                        applyTheme("purple")
                                    }
                                    style={{
                                        backgroundColor: "#9B59B6",
                                        borderColor: "#9B59B6",
                                        color: "white"
                                    }}
                                >
                                    적용
                                </Button>
                            ) : (
                                <Button
                                    onClick={() =>
                                        buyTheme("purple")
                                    }
                                    style={{
                                        backgroundColor: "#9B59B6",
                                        borderColor: "#9B59B6",
                                        color: "white"
                                    }}
                                >
                                    구매
                                </Button>
                              )}

                          </CardBody>
                        </Card>
                      </Col>

                    </Row>

                  </CardBody>
                </Card>
              </Col>
            </Row>
          </Container>
        </section>
      </main>

      <CardsFooter />
    </>
  );
}