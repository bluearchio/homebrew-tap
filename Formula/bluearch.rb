class Bluearch < Formula
  desc "BlueArch CLI - AWS infrastructure recommendations, alerting, and remediation"
  homepage "https://bluearch.io"
  version "0.0.0"
  license :cannot_represent

  depends_on arch: :arm64

  url "https://dist.bluearch.io/bluearch/latest/bluearch_macos_arm64"
  sha256 "PLACEHOLDER_SHA256"

  def install
    bin.install "bluearch_macos_arm64" => "bluearch"
  end

  def post_install
    # Clean up old curl-based installations if present
    old_binary = Pathname.new("#{Dir.home}/.local/bin/bluearch")
    if old_binary.exist?
      opoo "Removing old curl-installed binary at #{old_binary}"
      old_binary.unlink
    end
  end

  def caveats
    <<~EOS
      BlueArch CLI has been installed.

      Quick start:
        bluearch scan              # Scan AWS resources
        bluearch web start         # Launch web dashboard
        bluearch recommendations   # View findings

      Ensure your AWS credentials are configured:
        aws configure
        # or
        export AWS_PROFILE=your-profile
    EOS
  end

  test do
    system "#{bin}/bluearch", "--version-silent"
  end
end
