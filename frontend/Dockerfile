# deps + build stage 
FROM node:22-slim AS builder

WORKDIR /app

COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci

COPY frontend .

# the frontend needs to know the API URL at build time for
# NEXT_PUBLIC_ vars — passed in from docker-compose.yml as a build arg
ARG NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_API_URL=${NEXT_PUBLIC_API_URL}

RUN npm run build

# lean runtime stage
FROM node:22-slim AS runner

WORKDIR /app

ENV NODE_ENV=production

# standalone output includes only what's needed to run — a minimal
# server.js, the necessary node_modules subset, and build artifacts
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public

EXPOSE 3000

CMD ["node", "server.js"]