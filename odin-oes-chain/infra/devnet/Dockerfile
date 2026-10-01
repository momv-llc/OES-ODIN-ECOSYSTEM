FROM golang:1.25.9-bookworm AS build
WORKDIR /src
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -p 1 -o /out/oesd ./cmd/oesd

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates bash jq curl && rm -rf /var/lib/apt/lists/*
COPY --from=build /out/oesd /usr/local/bin/oesd
COPY infra/devnet/entrypoint.sh /usr/local/bin/oes-devnet-entrypoint
COPY infra/devnet/init.sh /usr/local/bin/oes-devnet-init
ENTRYPOINT ["/usr/local/bin/oes-devnet-entrypoint"]
