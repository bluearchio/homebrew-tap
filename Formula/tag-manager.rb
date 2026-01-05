class TagManager < Formula
  desc "AWS Tag Manager CLI - FinOps, compliance, and cost optimization tool"
  homepage "https://bluearch.io"
  url "https://dist.bluearch.io/tag-manager/v0.3.4/tag-manager_macos_arm64"
  version "v0.3.4"
  sha256 "07263cc77057965103c1a3cf8bbb4a684277e0334f469797ec06d1e29b008fe0"
  license :cannot_represent

  depends_on arch: :arm64

  def install
    bin.install "tag-manager_macos_arm64" => "tag-manager"
  end

  def post_install
    # Clean up curl-installed binary to avoid PATH conflicts
    # The curl installer puts the binary at ~/.local/bin/tag-manager
    curl_binary = Pathname.new(Dir.home) / ".local" / "bin" / "tag-manager"
    if curl_binary.exist?
      ohai "Removing old curl-installed binary at #{curl_binary}"
      curl_binary.unlink
    end
  end

  def caveats
    <<~EOS
      Tag Manager CLI has been installed.

      Getting started:
        tag-manager --help
        tag-manager setup validate

      Configure AWS credentials:
        export AWS_PROFILE=your-profile
        aws sso login

      Data is stored in: ~/.tag-manager/
    EOS
  end

  test do
    system "#{bin}/tag-manager", "--version"
  end
end
