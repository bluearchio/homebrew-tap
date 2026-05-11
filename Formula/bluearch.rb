class Bluearch < Formula
  desc "AWS infrastructure recommendations, alerting, and misconfig detection CLI"
  homepage "https://bluearch.io"
  url "https://dist.bluearch.io/bluearch/v0.12.4/bluearch_macos_arm64"
  version "v0.12.4"
  sha256 "059285907174239807a8a3ef9b6f02c7ff64ac50b3281465167e80999cfec842"
  license :cannot_represent

  depends_on arch: :arm64

  def install
    bin.install "bluearch_macos_arm64" => "bluearch"
  end

  def post_install
    # Clean up curl-installed binary to avoid PATH conflicts
    curl_binary = Pathname.new(Dir.home) / ".local" / "bin" / "bluearch"
    if curl_binary.exist?
      begin
        ohai "Removing old curl-installed binary at #{curl_binary}"
        curl_binary.unlink
        ohai "[OK] Old binary removed successfully"
      rescue Errno::EACCES
        opoo "Permission denied: Cannot remove #{curl_binary}"
        opoo "Run manually: rm ~/.local/bin/bluearch"
      rescue Errno::EBUSY
        opoo "File is in use: #{curl_binary}"
        opoo "Close any running bluearch processes, then run: rm ~/.local/bin/bluearch"
      rescue => e
        opoo "Could not remove #{curl_binary}: #{e.message}"
        opoo "Run manually: rm ~/.local/bin/bluearch"
      end
    end
  end

  def caveats
    <<~EOS
      BlueArch CLI has been installed.

      Getting started:
        bluearch --help
        bluearch scan

      Configure AWS credentials:
        export AWS_PROFILE=your-profile
        aws sso login

      Data is stored in: ~/.bluearch/
    EOS
  end

  test do
    system "#{bin}/bluearch", "--version"
  end
end
